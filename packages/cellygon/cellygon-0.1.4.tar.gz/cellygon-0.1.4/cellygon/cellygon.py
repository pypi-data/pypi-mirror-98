#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:56:01 2019

@author: henrik
"""

from imgmisc import validate_connectivity, validate_inputs, compute_neighbours, merge, autocrop, rand_cmap, flatten, get_resolution
from skimage.morphology import binary_dilation
from collections import defaultdict
from mahotas.labeled import relabel
from numba import jit, njit
import tifffile as tiff
import networkx as nx
import pyvista as pv
import mahotas as mh
import numpy as np
import vtk

def get_l1(seg_img, bg=0, selem=None):
    # TODO: Include option to remove cells bordering the image limits?
    bg_dilated = np.logical_and(binary_dilation(seg_img==bg, selem=selem), seg_img)
    
    labels = np.unique(seg_img)
    labels = labels[labels != bg]
    l1 = np.unique(seg_img[bg_dilated])
    l1 = l1[l1 != bg]
    l1 = np.isin(labels, l1)
    return l1

def get_layers(seg_img, bg=0, depth=None):
    labeled_img = seg_img.copy()
    layers = []

    while True:
        if depth is not None and len(layers) >= depth:
            break
        
        layer = get_l1(labeled_img, bg=bg)
        
        if sum(layer) == 0:
            continue
        layer_labels = np.unique(labeled_img)[1:][layer]
        layers.append(layer_labels)
        labeled_img[np.isin(labeled_img, layer_labels)] = bg
    return layers


def consolidate_disjoint_cells(j_indices, j_neighs, edges=None, background=0, allow_triangles=True, mode='compress'):
    # Get cell polygons and remove entries in j_neighs that don't make up complete cells
    iteration = 0
    while True:
        n_before = j_indices.shape[0]
        print(iteration)
        iteration += 1
        labels, label_counts = np.unique(flatten(j_neighs), return_counts=True)
        # labels = labels[label_counts > (2 if allow_triangles else 3)]
        labels = labels[labels != background]
        cells = {}
        to_merge = []
        for ii in labels:
            ii_in = np.where([ii in nn for nn in j_neighs])[0]
            # if edges is None:
            cell_edges = find_edges(j_indices[ii_in], j_neighs[ii_in])
            # else:
                # TODO - make this work with provided edges
                # pass
            net = nx.Graph()
            net.add_edges_from(cell_edges)
            cycles = nx.cycle_basis(net)
            breaking = False
            if len(cycles) > 1:
                for cc1, cyc1 in enumerate(cycles):
                    if breaking:
                        break
                    for cc2, cyc2 in enumerate(cycles):
                        if cc2 <= cc1:
                            continue
                        print(np.intersect1d(cyc1, cyc2).shape[0])
                        # if the cells have no overlap, or only connect by a single 
                        # vertex (e.g. due to cell overhang)
                        if np.intersect1d(cyc1, cyc2).shape[0] < 2:
                            to_merge.append(list(ii_in[np.array(cyc1)]) if len(cyc1) < len(cyc2) else list(ii_in[np.array(cyc2)]))
                            breaking=True
                            break
                        
            to_merge = merge(to_merge)
            to_remove = []
            for group in to_merge:
                group = np.asarray(list(group))
                j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
                j_indices[group[0]] = np.mean(j_indices[group], 0)
                to_remove.extend(list(group[1:]))
        to_keep = np.logical_not(np.isin(np.arange(j_indices.shape[0]), to_remove))
        j_indices = j_indices[to_keep]
        j_neighs = j_neighs[to_keep]
        
        if j_indices.shape[0] == n_before:
            break
    return j_indices, j_neighs

def get_connected_vertices(mesh, index, include_self=True):

    connected_vertices = []
    if include_self:
        connected_vertices.append(index)

    cell_id_list = vtk.vtkIdList()
    mesh.GetPointCells(index, cell_id_list)

    # Loop through each cell using the seed point
    for ii in range(cell_id_list.GetNumberOfIds()):
        cell = mesh.GetCell(cell_id_list.GetId(ii))

        if cell.GetCellType() == 3:
            point_id_list = cell.GetPointIds()

            # add the point which isn't the seed
            to_add = point_id_list.GetId(1) if point_id_list.GetId(0) == index else point_id_list.GetId(0)
            connected_vertices.append(to_add)
        else:
            # Loop through the edges of the point and add all points on these.
            for jj in range(cell.GetNumberOfEdges()):
                point_id_list = cell.GetEdge(jj).GetPointIds()

                # add the point which isn't the seed
                to_add = point_id_list.GetId(1) if point_id_list.GetId(0) == index else point_id_list.GetId(0)
                connected_vertices.append(to_add)

    connected_vertices = np.unique(connected_vertices)

    return connected_vertices

def get_connected_vertices_all(mesh, include_self=True):

    connectivities = [[]] * mesh.n_points
    for ii in range(mesh.n_points):
        connectivities[ii] = get_connected_vertices(mesh, ii, include_self)

    connectivities = np.array(connectivities)

    return connectivities
        

def consolidate_holes(tripoly, j_neighs, background=0, mode='all'):
    from phenotastic.mesh import get_boundary_points
    boundary = tripoly.extract_feature_edges(boundary_edges=1, feature_edges=0, feature_angle=0, manifold_edges=0, non_manifold_edges=0)
    bdpts = boundary.points
    indices = np.array([tripoly.FindPoint(ii) for ii in bdpts])
    from phenotastic.mesh import get_cycles
    cycles=  get_cycles(boundary)        
    cycles = [c for c in cycles if len(c) > 1]
    cycles = [[tripoly.FindPoint(bdpts[ii]) for ii in cyc] for cyc in cycles]
    
    prev_ids = tripoly['cell_id'].copy()
    added = 0
    new_pts = []
    new_faces = []
    new_cids = []
    for cyc in cycles[1:]:
        labs, cts = np.unique(np.asarray(flatten(j_neighs[np.array(cyc)]))[np.logical_not(np.isin(flatten(j_neighs[np.array(cyc)]), np.append(tripoly['cell_id'], background)))], return_counts=True)
        maxlab = labs[np.argmax(cts)]
        print(max(cts), len(cyc))
        if mode == 'largest' or (mode=='all' and max(cts) == len(cyc)):
            new_faces.extend(np.ravel([[3, cyc[cc-1], cyc[cc], tripoly.n_points + added] for cc in range(len(cyc))]))
            new_pts.append(np.mean(tripoly.points[cyc], 0))
            new_cids.extend([maxlab] * len(cyc))
            added += 1
    tripoly.points = np.vstack([tripoly.points, new_pts])
    tripoly.faces = np.hstack([tripoly.faces, np.hstack(new_faces)])
    tripoly['cell_id'] = np.hstack([prev_ids, new_cids])
    
    return tripoly        


def find_junctions_all(image, background=0, threshold=3, merge_adjacent=True, resolution=None, include_set='l1'):
    connectivity = 3
    if include_set == 'l1':
        include = get_layers(image, bg=background, depth=1)[0]
        
    image, mask, resolution = validate_inputs(image, mask=None, resolution=resolution)
    connectivity, offset = validate_connectivity(image.ndim, connectivity,
                                                  offset=None)
    mask = mh.borders(image, connectivity)

    # get the distances to the neighbours
    neighbours = connectivity.copy()
    neighbours[tuple(offset)] = False
    neighbours = np.array(np.where(neighbours)).T
    neighbours = np.multiply(neighbours, resolution)
    neighbours = np.subtract(neighbours, offset)

    # pad the image, and mask so that we can use the mask to keep from running
    # off the edges
    pad_width = [(p, p) for p in offset]
    image = image.astype(float) # to allow -1 padding
    image = np.pad(image, pad_width, mode='constant', constant_values=-1)
    mask = np.pad(mask, pad_width, mode='constant', constant_values=background)

    # get flattened versions of everything
    flat_neighbourhood = compute_neighbours(image, connectivity, offset)
    image_raveled = image.ravel()
    indices = np.where(mask.ravel())[0]
    
    point_neighbours = np.array(list(map(lambda x: x + flat_neighbourhood, indices)))
    neighs = image_raveled[point_neighbours]

    # Identify all voxels that neighbour at least 3 different cell ids and neighbour the background
    # TODO include option to include vertices that border both -1 and background
    # TODO generalise to not be restricted to epidermis
    # - TODO change hard-coding for L1 to other collections of labels as well
    junctions = []
    # to_keep = include
    for row in neighs:
        r = np.unique(row)
        # if background not in r:
            # junctions.append(False)
        # else:
        # r = r[np.isin(r, to_keep)]
        junctions.append(len(r) >= threshold)

    # Extract the vertex coordinates and information about what cells junctions belong to        
    j_indices_raveled = indices[junctions]
    j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
    j_neighs = np.asarray([np.unique(row) for row in neighs[junctions]])

    # Consolidate junctions that are neighbours with one another
    if merge_adjacent:
        to_merge = []
        for ii, pt in enumerate(point_neighbours[junctions]):
            for jj, nb in enumerate(pt):
                if nb in j_indices_raveled:
                    to_merge.append([ii, np.where(j_indices_raveled == nb)[0][0]])
        to_merge = merge(to_merge)
        to_remove = []
        new_coords = []
        for group in to_merge:
            group = np.asarray(list(group))
            j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
            new_coords.append(j_indices_raveled[group])
            to_remove.extend(list(group[1:]))
        
        keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
        j_indices_raveled = j_indices_raveled[keep_indices]
        j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
        j_neighs = j_neighs[keep_indices]
        
        merged_coords = np.asarray([np.mean(np.asarray(np.unravel_index(nc, image.shape)).T,0) for nc in new_coords])
        for ii, orig_coords in enumerate([np.asarray(np.unravel_index(nc[0], image.shape)).T for nc in new_coords]):
            j_indices[np.where(np.all(j_indices == orig_coords, 1))[0][0]] = merged_coords[ii]
        
    return j_indices, j_neighs

def merge_junctions_euclidean(j_indices, j_neighs, r):
    """ Merges junctions by euclidean distance (inclusive) """
    from scipy.spatial import KDTree
    tree = KDTree(j_indices)
    matches = tree.query_ball_tree(tree, r=r)
    to_merge = merge(matches)
    to_remove = []
    # j_neighs = np.array([vv for vv in j_neighs])
    j_neighs = list(j_neighs)
    for group in to_merge:
        group = np.asarray(list(group))
        j_neighs[group[0]] = np.unique(np.hstack([j_neighs[gg] for gg in group]))
        j_indices[group[0]] = np.mean(j_indices[group], 0)
        to_remove.extend(list(group[1:]))
        
    to_keep = np.logical_not(np.isin(np.arange(j_indices.shape[0]), to_remove))
    j_indices = j_indices[to_keep]
    j_neighs = np.array(j_neighs)[to_keep]
    return j_indices, j_neighs    


def find_junctions(image, background=0, threshold=3, merge_adjacent=True, resolution=None, include_set='l1'):

    connectivity = 3
    image, mask, resolution = validate_inputs(image, mask=None, resolution=resolution)
    connectivity, offset = validate_connectivity(image.ndim, connectivity,
                                                  offset=None)
    mask = mh.borders(image, connectivity)

    if include_set == 'l1':
        include = get_layers(image, bg=background, depth=1)[0]
    else:
        include= include_set

    # get the distances to the neighbours
    neighbours = connectivity.copy()
    neighbours[tuple(offset)] = False
    neighbours = np.array(np.where(neighbours)).T
    neighbours = np.multiply(neighbours, resolution)
    neighbours = np.subtract(neighbours, offset)

    # pad the image, and mask so that we can use the mask to keep from running
    # off the edges
    pad_width = [(p, p) for p in offset]
    image = image.astype(float) # to allow -1 padding
    image = np.pad(image, pad_width, mode='constant', constant_values=-1)
    mask = np.pad(mask, pad_width, mode='constant', constant_values=0)

    # get flattened versions of everything
    flat_neighbourhood = compute_neighbours(image, connectivity, offset)
    image_raveled = image.ravel()
    indices = np.where(mask.ravel())[0]
    
    point_neighbours = np.array(list(map(lambda x: x + flat_neighbourhood, indices)))
    neighs = image_raveled[point_neighbours]

    # Identify all voxels that neighbour at least 3 different cell ids and neighbour the background
    # TODO include option to include vertices that border both -1 and background
    # TODO generalise to not be restricted to epidermis
    # - TODO change hard-coding for L1 to other collections of labels as well
    junctions = []
    to_keep = include
    for row in neighs:
        r = np.unique(row)
        if background not in r:
            junctions.append(False)
        else:
            r = r[np.isin(r, to_keep)]
            junctions.append(len(r) >= threshold)

    # Extract the vertex coordinates and information about what cells junctions belong to        
    j_indices_raveled = indices[junctions]
    j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
    j_neighs = np.asarray([np.unique(row) for row in neighs[junctions]])

    # Consolidate junctions that are neighbours with one another
    if merge_adjacent:
        to_merge = []
        for ii, pt in enumerate(point_neighbours[junctions]):
            for jj, nb in enumerate(pt):
                if nb in j_indices_raveled:
                    to_merge.append([ii, np.where(j_indices_raveled == nb)[0][0]])
        to_merge = merge(to_merge)
        to_remove = []
        new_coords = []
        for group in to_merge:
            group = np.asarray(list(group))
            j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
            new_coords.append(j_indices_raveled[group])
            to_remove.extend(list(group[1:]))
        
        keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
        j_indices_raveled = j_indices_raveled[keep_indices]
        j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
        j_neighs = j_neighs[keep_indices]
        
        merged_coords = np.asarray([np.mean(np.asarray(np.unravel_index(nc, image.shape)).T,0) for nc in new_coords])
        for ii, orig_coords in enumerate([np.asarray(np.unravel_index(nc[0], image.shape)).T for nc in new_coords]):
            j_indices[np.where(np.all(j_indices == orig_coords, 1))[0][0]] = merged_coords[ii]
        
    return j_indices, j_neighs

def center_triangulation(j_indices, j_neighs, background, allow_triangles=True, return_ids=True):
    cpolys = polygon_cycles(j_indices, j_neighs, edges=None, background=background, allow_triangles=allow_triangles)
    cycles = np.asarray(list(cpolys.values()))
    centers = np.asarray([np.mean(j_indices[cycles[ii]], 0) for ii in range(len(cycles))])
    
    faces = []
    for ii, cyc in enumerate(cycles):
        for jj in range(len(cyc)):
            faces.append([cyc[jj-1], cyc[jj], j_indices.shape[0] + ii])
    faces = np.asarray(faces)
    j_coords = np.vstack([j_indices, centers])

    if return_ids:
        cell_ids = flatten([[list(cpolys.keys())[ii]] * (len(cycles[ii])) for ii in range(len(cycles))])
        return j_coords, faces, cell_ids
    return j_coords, faces


def merge_identical_junctions(j_indices, j_neighs):
    to_merge = []
    for ii, jneighs1 in enumerate(j_neighs):
        for jj, jneighs2 in enumerate(j_neighs):
            if jj <= ii:
                continue
            else:
                # overlap = np.intersect1d(jneighs1, jneighs2).shape[0]
                if len(jneighs1) == len(jneighs2) and np.all(np.sort(jneighs2) == np.sort(jneighs1)):
                    to_merge.append([ii,jj])
    to_merge = merge(to_merge)
    to_remove = []
    for group in to_merge:
        group = np.asarray(list(group))
        j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
        to_remove.extend(list(group[1:]))
    
    keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
    # j_indices_raveled = j_indices_raveled[keep_indices]
    j_indices = j_indices[keep_indices]
    j_neighs = j_neighs[keep_indices]
    return j_indices, j_neighs        

def merge_similar_junctions(j_indices, j_neighs, threshold=4):
    iteration = 0
    while True:
        print(iteration)
        iteration += 1
        n_before = j_indices.shape[0]
        to_merge = []
        for ii, jneighs1 in enumerate(j_neighs):
            for jj, jneighs2 in enumerate(j_neighs):
                if jj <= ii:
                    continue
                else:
                    overlap = np.intersect1d(jneighs1, jneighs2).shape[0]
                    if overlap >= threshold:
                        to_merge.append([ii, jj])
        to_merge = merge(to_merge)
        to_remove = []
        for group in to_merge:
            group = np.asarray(list(group))
            j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
            to_remove.extend(list(group[1:]))
        
        keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
        # j_indices_raveled = j_indices_raveled[keep_indices]
        j_indices = j_indices[keep_indices]
        j_neighs = j_neighs[keep_indices]
        
        if j_indices.shape[0] == n_before:
            break
        
    return j_indices, j_neighs        

def find_edges(j_indices, j_neighs, threshold=3):
    edges = []
    for ii, jneighs1 in enumerate(j_neighs):
        # print(ii / len(j_neighs))
        for jj, jneighs2 in enumerate(j_neighs):
            if jj <= ii:
                continue
            else:
                overlap = np.intersect1d(jneighs1, jneighs2).shape[0]
                if overlap >= threshold and [ii, jj] not in edges and [jj, ii] not in edges:
                    edges.append([ii, jj])
    
    # Remove edges to vertices that are only connected with one edge
    indices, counts = np.unique(edges, return_counts=True)
    to_keep = indices[counts > 1]
    edges = [edge for edge in edges if np.all(np.isin(edge, to_keep))]
    
    return edges

def remove_duplicated_vertices(j_indices, j_neighs):
    keep = []
    for ii, jn1 in enumerate(j_neighs):
        duplicated = False
        for jj, jn2 in enumerate(j_neighs):
            if jj > ii and np.all(jn1 == jn2):
                duplicated=True
                break
        keep.append(not duplicated)
    keep = np.asarray(keep)
    j_indices = j_indices[keep]
    j_neighs = j_neighs[keep]
    return j_indices, j_neighs

def triangle_area(verts):
    if verts.ndim < 2:
        verts = np.expand_dims(verts, 0)
    v1 = verts[:, 0, :] - verts[:, 1, :]
    v2 = verts[:, 0, :] - verts[:, 2, :]
    del verts
    
    # Area of a triangle in 3D is 1/2 * norm of the cross product
    area = ((np.cross(v1, v2) ** 2).sum(axis=1) ** 0.5) / 2.
    return area

def merge_triangles(j_indices, j_neighs, threshold=None):
    iteration = 0
    while True:
        print(iteration)
        iteration += 1
        
        init_len = j_indices.shape[0]
        edges = find_edges(j_indices, j_neighs)

        G = nx.Graph()
        G.add_edges_from(edges)
        cliques = nx.find_cliques(G)
        cliques = np.asarray([qq for qq in cliques if len(qq) == 3])

        areas = triangle_area(j_indices[cliques])
        to_remove = []
        for ii, qq in enumerate(cliques):
            if threshold is not None and areas[ii] < threshold:
                continue
            j_indices[qq[0]] = np.mean(j_indices[qq], 0)
            j_neighs[qq[0]] = np.unique(np.hstack(j_neighs[qq]))
            to_remove.extend(list(qq[1:]))
        j_indices = j_indices[np.logical_not(np.isin(np.arange(j_indices.shape[0]), to_remove))]
        j_neighs = j_neighs[np.logical_not(np.isin(np.arange(j_neighs.shape[0]), to_remove))]
        j_indices, j_neighs = merge_similar_junctions(j_indices, j_neighs)
        
        if init_len == j_indices.shape[0]:
            break

    return j_indices, j_neighs, edges

def clean(j_indices, j_neighs, return_edges=True):
    while True:
        n_before = j_indices.shape[0]
        # j_indices, j_neighs = merge_similar_junctions(j_indices, j_neighs)
        edges = find_edges(j_indices, j_neighs)
        
        junctions = np.arange(len(j_indices))
        in_edges, counts = np.unique(edges, return_counts=True)
        to_keep = np.isin(junctions, in_edges)
        
        j_indices = j_indices[to_keep]
        j_neighs = j_neighs[to_keep]
        
        j_indices = j_indices[counts > 1]
        j_neighs = j_neighs[counts > 1]
        
        if j_indices.shape[0] == n_before:
            break
    
    if not return_edges:
        return j_indices, j_neighs
    else:
        edges = find_edges(j_indices, j_neighs)
        return j_indices, j_neighs, edges

def create_polydata(j_indices, faces, resolution=[1,1,1]):
    poly = pv.PolyData(j_indices * resolution, np.ravel(np.c_[[len(ff) for ff in faces], faces]))
    return poly

def problematic_vertices(j_indices, j_neighs, edges=None, background=0, threshold=4):
    # Identify all vertices that has more than two connections to the same cell id
    if edges is None:
        edges = find_edges(j_indices, j_neighs)
    poly = create_polydata(j_indices, edges)
    neighs = get_connected_vertices_all(poly, True)
    problematic = []
    for ii, ji in enumerate(j_indices):
        nneighs = np.hstack(j_neighs[neighs[ii]])
        nneighs = nneighs[nneighs != background]
        vals, counts = np.unique(nneighs, return_counts=True)
        if any(counts >= threshold):
            problematic.append(ii)
    problematic = np.asarray(problematic)
    return problematic

def polygon_cycles(j_indices, j_neighs, edges=None, background=0, allow_triangles=True):
    # Get cell polygons and remove entries in j_neighs that don't make up complete cells
    labels, label_counts = np.unique(flatten(j_neighs), return_counts=True)
    labels = labels[label_counts > (2 if allow_triangles else 3)]
    labels = labels[labels != background]
    cells = {}
    for ii in labels:
        ii_in = np.where([ii in nn for nn in j_neighs])[0]
        if edges is None:
            cell_edges = find_edges(j_indices[ii_in], j_neighs[ii_in])
        else:
            # TODO - make this work with provided edges
            pass
        net = nx.Graph()
        net.add_edges_from(cell_edges)
        cycles = nx.cycle_basis(net)
        if len(cycles) == 1:
            cycle = ii_in[cycles[0]]
            cells[ii] = cycle
    return cells

def unit_vec(vector):
    return vector / np.linalg.norm(vector)

def angle(v1, v2, v3):
    u = unit_vec(np.array(v1) - np.array(v2))
    v = unit_vec(np.array(v3) - np.array(v2))
    return np.arccos(np.clip(np.dot(u, v), -1, 1)) / (2 * np.pi) * 360

def proj_to_plane(point, v1, v2, v3):
    # Project point onto the plane defined by v1, v2, v3
    new_i = unit_vec(np.array(v1) - np.array(v2))
    new_j = unit_vec(np.array(v3) - np.array(v2))
    new_k = np.cross(new_i, new_j)
    change_of_basis = np.array([new_i, new_j, new_k]).transpose()
    point = np.array(
        [[point[0] - v2[0]], [point[1] - v2[1]], [point[2] - v2[2]]])
    point_in_new_basis = np.dot(np.linalg.inv(change_of_basis), point)
    proj_in_new_basis = np.copy(point_in_new_basis)
    proj_in_new_basis[2, 0] = 0
    proj = ((np.dot(change_of_basis, proj_in_new_basis) +
             np.array([[v2[0]], [v2[1]], [v2[2]]]))).flatten().tolist()
    return proj

def internal_angles_mesh(cellygon_mesh, background=0, mode='project'):
    # poly = create_polydata(j_indices, edges)
    # vertex_labels
    neighs = get_connected_vertices_all(cellygon_mesh, include_self=False)
    cells = np.unique(cellygon_mesh['cell_id'])
    
    points = cellygon_mesh.points
    faces = cellygon_mesh.faces.reshape((-1, 4))[:, 1:]
    faces_cell_ids = np.c_[cellygon_mesh['cell_id'], 
                           cellygon_mesh['cell_id'], 
                           cellygon_mesh['cell_id']]
    
    all_angles = []
    for cell in cells:
        cell_faces = faces[np.all(faces_cell_ids == cell, 1)]
        vids, cts = np.unique(cell_faces, return_counts=True)
 
        # TODO remove indices that are in all, rather than max
        vids = np.delete(vids, np.argmax(cts)) # don't consider center
        
        for vid in vids:
            v_neighs = points[neighs[vid][np.isin(neighs[vid], vids)]]
            phi = angle(v_neighs[0], points[vid], v_neighs[1])
            all_angles.append([cell, vid, phi])
    all_angles = np.array(all_angles)
    return all_angles
    
#     # for cell in cells:
#     #     angles = 
    

#     output = []
#     for ii, cell in enumerate(np.unique(cells)):
#         for jj in np.where(np.array([any(jn == cell) for jn in j_neighs]))[0]:
#             v_neighs = [nn for nn in neighs[jj]]
#             v_neighs_in_cell = [vv for vv in v_neighs if cell in j_neighs[vv]]
#             n_neighs, n_neighs_in_cell = len(v_neighs), len(v_neighs_in_cell)
            
#             if n_neighs_in_cell != 2:
#                 print('Warning: vertex {ii} has too many neighbours in the same cell. Ignoring...')
#                 continue
#             v1 = j_indices[v_neighs_in_cell[0]] - j_indices[jj]
#             v1 = v1 / np.linalg.norm(v1)
#             v2 = j_indices[v_neighs_in_cell[1]] - j_indices[jj]
#             v2 = v2 / np.linalg.norm(v2)
#             phi = np.arccos(np.dot(v1, v2)) / (2 * np.pi) * 360
#             # if n_neighs == 2:
#             #     # define plane using only neighbouring same-cell vertices
#             #     phi = angle(j_indices[v_neighs_in_cell[0]], 
#             #                   j_indices[jj], 
#             #                   j_indices[v_neighs_in_cell[1]])
#             # else:
#             #     # define plane using all neighbouring vertices
                
#             #     phi = angle(j_indices[v_neighs_in_cell[0]], 
#             #                   proj_to_plane(j_indices[jj], 
#             #                                 j_indices[v_neighs_in_cell[0]], 
#             #                                 j_indices[v_neighs_in_cell[1]], 
#             #                                 np.mean(j_indices[v_neighs], 0)), 
#             #                   j_indices[v_neighs_in_cell[1]])
#             output.append((cell, jj, v_neighs_in_cell[0], v_neighs_in_cell[1], phi, n_neighs))
#     output = np.asarray(output)
#     return output



def internal_angles(j_indices, j_neighs, edges, cells=None, background=0, mode='project'):
    poly = create_polydata(j_indices, edges)
    neighs = get_connected_vertices_all(poly, include_self=False)
    
    if cells is None:
        # TODO: write convenience function for this
        _, _, cells = center_triangulation(j_indices, j_neighs, background)
        cells = np.unique(cells)

    output = []
    for ii, cell in enumerate(np.unique(cells)):
        for jj in np.where(np.array([any(jn == cell) for jn in j_neighs]))[0]:
            v_neighs = [nn for nn in neighs[jj]]
            v_neighs_in_cell = [vv for vv in v_neighs if cell in j_neighs[vv]]
            n_neighs, n_neighs_in_cell = len(v_neighs), len(v_neighs_in_cell)
            
            if n_neighs_in_cell != 2:
                print('Warning: vertex {ii} has too many neighbours in the same cell. Ignoring...')
                continue
            v1 = j_indices[v_neighs_in_cell[0]] - j_indices[jj]
            v1 = v1 / np.linalg.norm(v1)
            v2 = j_indices[v_neighs_in_cell[1]] - j_indices[jj]
            v2 = v2 / np.linalg.norm(v2)
            phi = np.arccos(np.dot(v1, v2)) / (2 * np.pi) * 360
            # if n_neighs == 2:
            #     # define plane using only neighbouring same-cell vertices
            #     phi = angle(j_indices[v_neighs_in_cell[0]], 
            #                   j_indices[jj], 
            #                   j_indices[v_neighs_in_cell[1]])
            # else:
            #     # define plane using all neighbouring vertices
                
            #     phi = angle(j_indices[v_neighs_in_cell[0]], 
            #                   proj_to_plane(j_indices[jj], 
            #                                 j_indices[v_neighs_in_cell[0]], 
            #                                 j_indices[v_neighs_in_cell[1]], 
            #                                 np.mean(j_indices[v_neighs], 0)), 
            #                   j_indices[v_neighs_in_cell[1]])
            output.append((cell, jj, v_neighs_in_cell[0], v_neighs_in_cell[1], phi, n_neighs))
    output = np.asarray(output)
    return output


# fname = '/home/henrikahl/180316-PIN1_GFP-myr_YFP-WT-SAM1-FM8_stackreg_crop_wiener_C1_predictions_gasp_average.tiff'
# from imgmisc import listdir
# files = listdir("/home/henrikahl/projects/pin_patterns/data/final/segmentation/131007-PIN_GFP-acyl_YFP-Timelapse_4h-WT/", sorting='natural', include='.tif')
# fname = "/home/henrikahl/projects/pin_patterns/data/final/segmentation/131007-PIN_GFP-acyl_YFP-Timelapse_4h-WT/131007-PIN_GFP-acyl_YFP-plant_3-0h_stackreg_crop_wiener_C0_predictions_multicut_refined.tif"
# fname = files[1]
# data = tiff.imread(fname)

# resolution =  get_resolution(fname) #np.array([0.1735086, 0.1735086, 0.12529532381630637])[::-1]

# # data = data[100:, :250, 50:250]
# data = autocrop(data, 0, n=1)
# data = relabel(data)[0] 
# data -= np.min(data)

# data = relabel(data)[0] 
# contour = data > np.min(data)
# mesh = create_mesh(contour, resolution=resolution)
# mesh = mesh.extract_largest()
# mesh = mesh.clean()
# # mesh = make_manifold(mesh, 50)

# # mesh = mesh.decimate(.5)
# mesh = remesh(mesh, mesh.n_points // 2, sub=0)
# from phenotastic.mesh import repair_small
# from phenotastic.mesh import get_connected_vertices_all
# from imgmisc import matching_rows
# from imgmisc import merge
# mesh = mp.repair_small(mesh, 100)
# mesh = mesh.clean()
# mesh = make_manifold(mesh, 50)
# mesh = mesh.fill_holes(30)
# mesh = mesh.clean()

# v_neighbours = get_connected_vertices_all(mesh, False)
# boundary_indices = boa.get_boundary_points(mesh)

# # mesh = remesh(mesh, mesh.n_points // 2, sub=0)
# print(f'Labelling mesh')
# labels = label_mesh(mesh, data, resolution=resolution, mode='point', bg=np.min(data))
# mesh['labels'] = labels
   
# # @jit
# def find_junctions(labels, v_neighbours, boundary_indices, verbose=True):
#     junctions = {}
#     for vv in range(mesh.n_points):
#         neighbouring_labels = np.unique(labels[v_neighbours[vv]])
#         n_neighs = len(neighbouring_labels)
        
#         # Junctions on the boundary only need to border one other cell. Otherwise
#         # junctions need to border at least 3 cells.
#         if n_neighs > 2:# or (vv in boundary_indices and n_neighs > 1):
#             junctions[vv] = neighbouring_labels.astype(np.int_)
            
#             if verbose:
#                 print(str(vv) + ' is a junction')

#     return junctions

# # @njit
# def junctions2edges(junctions, boundary_indices):
#     verts = list(junctions.keys())
#     neighs = list(junctions.values())
    
#     edges = []
#     for ii in range(len(verts)):
#         ii_in_boundary = verts[ii] in boundary_indices
#         # ii_in_boundary = len(neighs) == 2
#         for jj in range(ii + 1, len(verts)):
            
#             overlap = sum([neighs[ii][kk] in neighs[jj] for kk in range(len(neighs[ii]))])
            
#             if overlap > 1:
#                 edges.append([verts[ii], verts[jj]])
#             else:
#                 if overlap == 1 and ii_in_boundary and verts[jj] in boundary_indices:
#                     edges.append([verts[ii], verts[jj]])
#     edges = np.array(edges, dtype='int')
#     return edges

# # @jit
# def merge_adjacent_junctions(mesh, junctions, edges):
#     v_neighbours = get_connected_vertices_all(mesh, False)
    
#     j_indices = list(junctions.keys())
#     to_merge = []
#     for vv, doms in junctions.items():
#         nn = v_neighbours[vv][np.isin(v_neighbours[vv], j_indices)]
#         if len(nn) != 0:
#             to_merge.append([vv] + list(nn))
#     to_merge = np.array([list(ff) for ff in merge(to_merge)])
#     to_merge = [np.unique(ll) for ll in to_merge]
    
#     for mm in to_merge:
#         center = np.mean(mesh.points[mm], axis=0)
#         edges[np.isin(edges, mm[1:])] = mm[0]
#         new_neighs = np.unique(flatten([junctions[ii] for ii in mm]))
#         junctions[mm[0]] = new_neighs
#         mesh.points[mm[0]] = center
#         for jj in mm[1:]:
#             del junctions[jj]
            
#     return junctions, edges

# def get_centroids(mesh, junctions, labels):
#     # This is ridiculously stupid
#     # j_vals = list(junctions.values())
#     alls = {}
#     for lab in np.unique(labels):
#         print(lab)
#         indices = []
#         for vv, neighs in junctions.items():
#             if lab in neighs:
#                 indices.append(vv)
#         if len(indices) > 2:
#             alls[lab] = np.unique(indices)

#     centroids = np.array([np.mean(mesh.points[item], 0) for item in alls.values()])
#     return centroids

# def junctions2coords(junctions, mesh):
#     coords = np.array([mesh.points[ii] for ii in list(junctions.keys())])
#     return coords

# def relabel_wireframe(junctions, edges, return_mapping=False):
#     # pts = []
#     seen = {}
#     new_edges = []
#     last = -1
#     new_junctions = {}
#     for edge in edges:
#         if edge[0] not in seen:
#             seen[edge[0]] = last + 1
#             new_junctions[last + 1] = junctions[edge[0]]
#             last += 1
#             # pts.append(mesh.points[edge[0]])
#         if edge[1] not in seen:
#             seen[edge[1]] = last + 1
#             new_junctions[last + 1] = junctions[edge[1]]
#             last += 1
#             # pts.append(mesh.points[edge[1]])
#         new_edges.append([seen[edge[0]], seen[edge[1]]])
#     # pts = np.array(pts)
#     new_edges = np.array(new_edges)
    
#     if return_mapping:
#         return new_junctions, new_edges, seen
    
#     return new_junctions, new_edges

# # @jit
# def clean_edges(edges):
#     edges = edges[edges[:,0] != edges[:,1]] 
#     edges = np.unique(edges, axis=0)
#     # duplicates = matching_rows(edges[:,::-1], edges)
#     # edges = edges[duplicates[:, 0]]
#     return edges

# # @jit
# def poly2fan(mesh, junctions, labels, edges):
#     # This is ridiculously stupid
#     # new_edges = [list(ee) for ee in edges]
#     new_edges = []
#     # j_vals = list(junctions.values())
#     new_pts = []
#     seen = {}
#     last = -1
#     centroids = []
#     cell_labels = []
#     for lab in np.unique(labels):
#         print(lab)
#         indices = []
#         for vv, neighs in junctions.items():
#             if lab in neighs:
#                 indices.append(vv)
#         indices = np.unique(indices)
#         if len(indices) > 2:
#             for ind in indices:
#                 if ind not in seen:
#                     seen[ind] = last + 1
#                     last += 1
#                     new_pts.append(mesh.points[ind])
            
#             to_add = np.where(np.isin(edges, indices).sum(1) == 2)[0]
#             for ee in to_add:
#                 new_edges.append([seen[vv] for vv in edges[ee]] + [last + 1])
#                 cell_labels.append(lab)
#             avg_pos = np.mean(mesh.points[indices], 0)
#             new_pts.append(avg_pos)
#             centroids.append(avg_pos)
#             last +=  1
#     new_pts = np.array(new_pts)
#     centroids = np.array(centroids)
#     cell_labels = np.array(cell_labels)
#     new_edges = np.array(new_edges)

#     return new_pts, new_edges, centroids, cell_labels

# def correct_duplicate_junctions(junctions, edges):
#     import collections
#     junctions = junctions.copy()
#     elems = [tuple(np.sort(tt)) for tt in list(junctions.values())]
#     duplicated = list(set([x for x in elems if elems.count(x) > 1]))
#     j_keys = np.array(list(junctions.keys()))
    
#     while len(duplicated) > 0:
#         for elem in duplicated:
#             indices = j_keys[np.array([i for i, tupl in enumerate(elems) if tupl == tuple(elem)])]
#             junctions[indices[0]] = np.unique(flatten([junctions[vv] for vv in indices]))
#             for edge in edges:
#                 if edge[0] in indices[1:]:
#                     edge[0] = indices[0]
#                 if edge[1] in indices[1:]:
#                     edge[1] = indices[0]
#             for jj in indices[1:]:
#                 del junctions[jj]
#         j_keys = np.array(list(junctions.keys()))
#         elems = [tuple(np.sort(tt)) for tt in list(junctions.values())]
#         duplicated = list(set([x for x in elems if elems.count(x) > 1]))
#         print(len(duplicated))
        
#     return junctions, edges

# junctions = find_junctions(labels, v_neighbours, boundary_indices) # Identify junctions with corresponding cell neighbours
# edges = junctions2edges(junctions, boundary_indices.astype(np.int_)) # Use information of cell neighbourhoods to connect vertices
# j1, e1 = merge_adjacent_junctions(mesh, junctions, edges) # Merge adjacent junctions (to avoid self-crossing due to single-triangle cells)
# e2 = clean_edges(e1) # remove duplicate faces etc. 
# j2, e3 = correct_duplicate_junctions(j1, e2)
# j3, e4, mapping = relabel_wireframe(j2, e3, return_mapping=True)

# # Can't quite remember what this does
# e5 = []
# for ii in range(e4.shape[0]):
#     v = 0
#     for jj in range(ii+1, e4.shape[0]):
#         if all(e4[ii] == e4[jj][::-1]):
#             v = 1
#             break
#     if v == 0:
#         e5.append(e4[ii])
# e5 = np.array(e5)    
# v_coords = junctions2coords(mapping, mesh)

# # e5 are the final edges
# # j3 are the corresponding junctions and which original labels they were bordering
# # v_coords are the coordinates for the final vertices

# wireframe_poly = pv.PolyData(v_coords, np.array(flatten(np.c_[[len(ee) for ee in e5], e5])))


# # # uni, cts = np.unique(flatten(e4), return_counts=True)
# # keys = list(junctions.values())
# # cellygons = []
# # inv_map = {v: k for k, v in mapping.items()}
# # for ii in np.unique(labels):
# #     juncts = [key for key, val in j3.items() if ii in val]
# #     if len(juncts) > 2:     
# #         cellygons.append(juncts)    

# # # cellygons = [mapping[]]
# # candidates = []
# # for ii, cell in enumerate(cellygons):
# #     for idx in cell:
# #         row, col = np.where((e4 == idx))
# #         isin = np.isin(cell, e4[row, np.remainder(col + 1, 2)])
# #         if sum(isin) > 2:
# #             candidates.append((ii, idx))

# # cc = np.unique([c[1] for c in candidates])

# # cell_pts = [b.points[np.array(cellygons[cand[0]])] for cand in candidates]
# # cell_pts = np.vstack(cell_pts)

# # d = b.points[cc]

# #     # pass
# #     # for idx in cell:
                

    
# # # d = np.array([mesh.points[ii] for ii in p[-2]])
    

# # # junctions1, edges1 = merge_adjacent_junctions(mesh, junctions, edges) # Merge adjacent junctions (to avoid self-crossing due to single-triangle cells)
# # # edges2 = clean_edges(edges1) # remove duplicate faces etc. 

# # # edges = edges2
# # # def get_edge_mappings(junctions, edges):
# # #     pts = []
# # #     for edge in edges:
# # #         print(np.intersect1d(junctions[edge[0]], junctions[edge[1]]))
# # #         if np.intersect1d(junctions[edge[0]], junctions[edge[1]]).shape[0] > 2:
# # #             for ii in edge:#np.intersect1d(junctions[edge[0]], junctions[edge[1]]):
# # #                 pts.append(mesh.points[ii])
    
    
# # # new_pts, new_edges, centroids, cell_labels = poly2fan(mesh, junctions1, labels, edges2) # go from wireframe (polygons) to fan-based mesg

# # # def cellygon2tissue(fname, mesh, edge_data=None, cell_data=None, edge_lengths=None):
# # #     f = open('test.dat', 'w')
    
# # # a = pv.PolyData(np.asarray(new_pts), np.array(flatten(np.c_[[len(ee) for ee in new_edges], new_edges])))
# # # assert(a.n_points == a.clean().n_points and a.n_cells == a.clean().n_cells)
# # # a = a.clean() # shouldn't do anything
# # # poly = pv.PolyData(np.asarray(pts), np.ravel(np.c_[[2]*len(new_edges), new_edges]))
# # # poly = pv.PolyData(total_pts, total_faces)
# # # poly = poly.clean()


# #     pv.set_plot_theme('document')
# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     p.set_background('w')
# #     p.add_mesh(mesh, cmap=cmap, interpolate_before_map=False)
# #     p.view_yz()
# #     p.show()
    
# #     pv.set_plot_theme('document')
# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     p.set_background('w')
# #     p.add_mesh(mesh, cmap=cmap, interpolate_before_map=False)
# #     p.add_points(mesh.points[np.asarray(list(junctions.keys()))], color='r', render_points_as_spheres=True, point_size=5)
# #     p.view_yz()
# #     p.show()

# #     pv.set_plot_theme('document')
# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     p.set_background('w')
# #     p.add_mesh(mesh, cmap=cmap, interpolate_before_map=False)
# #     p.add_points(b.points[np.asarray(list(j3))], color='r', render_points_as_spheres=True, point_size=5)
# #     p.view_yz()
# #     p.show()

# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     p.set_background('w')
# #     p.add_mesh(b, opacity=1, lighting=0, color='blue', line_width=4,interpolate_before_map=False)
# #     p.add_points(b.points[np.asarray(list(j3))], color='r', render_points_as_spheres=True, point_size=5)
# #     p.view_yz()
# #     p.show()
    
# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     p.set_background('w')
# #     p.add_mesh(mesh, cmap=cmap, interpolate_before_map=False)
# #     p.add_mesh(b, opacity=1, lighting=0, color='blue', line_width=4,interpolate_before_map=False)
# #     p.add_points(b.points[np.asarray(list(j3))], color='r', render_points_as_spheres=True, point_size=5)
# #     p.view_yz()
# #     p.show()
    
# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     p.set_background('w')
# #     p.add_mesh(mesh, cmap=cmap, interpolate_before_map=False)
# #     p.add_mesh(b, opacity=1, lighting=0, color='blue', line_width=4,interpolate_before_map=False)
# #     p.add_points(b.points[np.asarray(list(j3))], color='r', render_points_as_spheres=True, point_size=30)
# #     p.view_yz()
# #     p.show()

# #     cmap = rand_cmap(len(np.unique(labels)), first_color_black=False)
# #     import pyvistaqt as pvqt
# #     p = pvqt.BackgroundPlotter(notebook=False)
# #     # p.set_background('gray')
# #     p.add_points(b.points[np.asarray(list(j3))], color='r', render_points_as_spheres=True, point_size=30)
# #     # p.add_points(np.array(centroids), color='g', render_points_as_spheres=True, point_size=10)
# #     p.add_mesh(mesh, cmap=cmap, interpolate_before_map=False)
# #     # cmap_cl = rand_cmap(len(np.unique(cell_labels)), first_color_black=False)
# #     # p.add_mesh(a, opacity=1, lighting=0, color='w', line_width=1, scalars=np.array(cell_labels), cmap=cmap_cl, interpolate_before_map=False)
# #     p.add_mesh(b, opacity=1, lighting=0, color='w', line_width=2,interpolate_before_map=False)
# #     p.add_points(d, color='b', render_points_as_spheres=True, point_size=30)
# #     # p.add_points(cell_pts, color='g', render_points_as_spheres=True, point_size=25)

# #     # p.add_mesh(a.extract_edges(0, 0, 1, 0, 0), opacity=1, lighting=0, color='orange', line_width=1, interpolate_before_map=False)
    
# #     # p.add_points(np.array(pts), color='b', render_points_as_spheres=True, point_size=20)
# #     from phenotastic.mesh import get_boundary_edges
# #     # a_boundary = get_boundary_edges(a)
# #     # p.add_mesh(poly, opacity=1, lighting=0, color='w', line_width=1)
# #     p.show()
    
# # p = pvqt.BackgroundPlotter(notebook=False)
# # # p.set_background('gray')
# # p.add_points(mesh.points[np.asarray(list(junctions))], color='r', render_points_as_spheres=True, point_size=10)
# # p.add_points(np.array(centroids), color='g', render_points_as_spheres=True, point_size=10)
# # p.add_mesh(mesh, opacity=1, cmap=cmap, interpolate_before_map=False)
# # cmap_cl = rand_cmap(len(np.unique(cell_labels)), first_color_black=False)
# # p.add_mesh(a, opacity=1, lighting=0, color='w', line_width=1, scalars=np.array(cell_labels), cmap=cmap_cl, interpolate_before_map=False)
# # # p.add_points(np.array(strange_pts), color='b', render_points_as_spheres=True, point_size=20)
# # from phenotastic.mesh import get_boundary_edges
# # # a_boundary = get_boundary_edges(a)


# # # p.add_mesh(poly, opacity=1, lighting=0, color='w', line_width=1)
# # p.show()

# # # poly.save(fname[:-4] + '.vtk')

# # ##TODO:
# # # Correct faces to include centroids
# # # Make script to convert to tissue


# # # def array_row_intersection(a,b):
# # #    tmp=np.prod(np.swapaxes(a[:,:,None],1,2)==b,axis=2)
# #    return a[np.sum(np.cumsum(tmp,axis=0)*tmp==1,axis=1).astype(bool)]

# # def fitPlaneLTSQ(XYZ):
# #     (rows, cols) = XYZ.shape
# #     G = np.ones((rows, 3))
# #     G[:, 0] = XYZ[:, 0]  #X
# #     G[:, 1] = XYZ[:, 1]  #Y
# #     Z = XYZ[:, 2]
# #     (a, b, c),resid,rank,s = np.linalg.lstsq(G, Z)
# #     normal = (a, b, -1)
# #     nn = np.linalg.norm(normal)
# #     normal = normal / nn
# #     return (c, normal)
