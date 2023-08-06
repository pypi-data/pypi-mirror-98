# coding: utf-8

# In general Geoformat is licensed under an MIT/X style license with the
# following terms:
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Authors :
#   Guilhain Averlant
#   Eliette Catelin
#   Quentin Lecuire
#   Charlotte Montesinos Chevalley
#   Coralie Rabiniaux

import sys

# GEOFORMAT conf variables
from geoformat_lib.conf.driver_variable import (
    OGR_FORMAT_CSV,
    OGR_FORMAT_KML,
    OGR_FORMAT_POSTGRESQL,
    OGR_FORMAT_GEOJSON,
    OGR_FORMAT_XLSX,
    OGR_FORMAT_ESRI_SHAPEFILE,
    OGR_DRIVER_NAMES)

from geoformat_lib.conf.geometry_variable import GEOMETRY_TYPE, GEOMETRY_CODE_TO_GEOMETRY_TYPE, GEOFORMAT_GEOMETRY_TYPE

# predicates
from geoformat_lib.geoprocessing.connectors.predicates import (
    point_intersects_point,
    point_intersects_segment,
    point_intersects_bbox,
    segment_intersects_bbox,
    segment_intersects_segment,
    bbox_intersects_bbox,
    point_position_segment,
    ccw_or_cw_segments
)

# operations
from geoformat_lib.geoprocessing.connectors.operations import (
    coordinates_to_point,
    coordinates_to_segment,
    coordinates_to_bbox,
    segment_to_bbox
)

# Geoprocessing

# measure
# distance
from geoformat_lib.geoprocessing.measure.distance import (
    euclidean_distance,
    manhattan_distance,
    point_vs_segment_distance,
    euclidean_distance_point_vs_segment
)
# length
from geoformat_lib.geoprocessing.measure.length import segment_length
from geoformat_lib.geoprocessing.length import geometry_length

# area
from geoformat_lib.geoprocessing.measure.area import shoelace_formula
from geoformat_lib.geoprocessing.area import geometry_area

# matrix
from geoformat_lib.geoprocessing.matrix.adjacency import (
    create_adjacency_matrix,
    get_neighbor_i_feat,
    get_area_intersecting_neighbors_i_feat
)

# line merge
from geoformat_lib.geoprocessing.line_merge import line_merge

# merge geometries
from geoformat_lib.geoprocessing.merge_geometries import merge_geometries

# split
from geoformat_lib.geoprocessing.split import (
    segment_split_by_point,
    linestring_split_by_point
)

# union
from geoformat_lib.geoprocessing.union import (
    union_by_split
)

# geoparameters -> lines
from geoformat_lib.geoprocessing.geoparameters.lines import (
    line_parameters,
    perpendicular_line_parameters_at_point,
    point_at_distance_with_line_parameters,
    crossing_point_from_lines_parameters
)

# boundaries
from geoformat_lib.geoprocessing.geoparameters import boundaries

# geoparameters -> bbox
from geoformat_lib.geoprocessing.geoparameters.bbox import (
    bbox_union,
    extent_bbox,
    point_bbox_position
)

# bbox conversion
from geoformat_lib.conversion.bbox_conversion import (
    envelope_to_bbox,
    bbox_to_envelope,
    bbox_extent_to_2d_bbox_extent,
    bbox_to_polygon_coordinates
)

# bytes conversion
from geoformat_lib.conversion.bytes_conversion import (
    int_to_4_bytes_integer,
    float_to_double_8_bytes_array,
    coordinates_list_to_bytes,
    double_8_bytes_to_float,
    integer_4_bytes_to_int
)

# coordinates conversion
from geoformat_lib.conversion.coordinates_conversion import (
    format_coordinates,
    coordinates_to_2d_coordinates
)

# features conversion
from geoformat_lib.conversion.feature_conversion import (
    feature_serialize,
    feature_deserialize,
    features_geometry_ref_scan,
    features_fields_type_scan,
    feature_list_to_geolayer,
    feature_filter_geometry,
    feature_filter_attributes,
    feature_filter,
    features_filter
)

# fields conversion
from geoformat_lib.conversion.fields_conversion import (
    update_field_index,
    recast_field,
    drop_field
)

# geolayer conversion
from geoformat_lib.conversion.geolayer_conversion import (
    multi_geometry_to_single_geometry_geolayer,
    geolayer_to_2d_geolayer,
    create_geolayer_from_i_feat_list,
)

# geometry conversion
from geoformat_lib.conversion.geometry_conversion import (
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection,
    multi_geometry_to_single_geometry,
    ogr_geometry_to_geometry,
    geometry_to_ogr_geometry,
    geometry_to_wkb,
    wkb_to_geometry,
    wkt_to_geometry,
    geometry_to_wkt,
    force_rhr,
    geometry_to_bbox,
    reproject_geometry
)

# metadata conversion
from geoformat_lib.conversion.metadata_conversion import (
    geometries_scan_to_geometries_metadata,
    fields_scan_to_fields_metadata,
    reorder_metadata_field_index_after_field_drop
)

# precision tolerance conversion
from geoformat_lib.conversion.precision_tolerance_conversion import (
    deduce_rounding_value_from_float,
    deduce_precision_from_round
)

# segment conversion
from geoformat_lib.conversion.segment_conversion import (
    segment_list_to_linestring
)

# database operation
from geoformat_lib.db.db_request import (
    sql,
    sql_select_to_geolayer
)

# geometry conversion
from geoformat_lib.conversion.geometry_conversion import (
    bbox_extent_to_2d_bbox_extent,
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection
)

# data printing
from geoformat_lib.explore_data.print_data import (
    get_features_data_table_line,
    print_features_data_table,
    get_metadata_field_table_line,
    print_metadata_field_table
)
# random geometries
from geoformat_lib.explore_data.random_geometry import (
    random_point,
    random_segment,
    random_bbox
)
# attributes index
from geoformat_lib.index.attributes.hash import (
    create_attribute_index
)

# grid index
from geoformat_lib.index.geometry.grid import (
    bbox_to_g_id,
    point_to_g_id,
    g_id_to_bbox,
    g_id_to_point,
    g_id_neighbor_in_grid_index,
    create_grid_index,
    grid_index_to_geolayer
)

# driver
from geoformat_lib.driver.ogr.ogr_driver import (
    ogr_layer_to_geolayer,
    ogr_layers_to_geocontainer,
    geolayer_to_ogr_layer,
    geocontainer_to_ogr_format
)

# clauses
from geoformat_lib.processing.data.clauses import (
    clause_group_by,
    clause_where,
    clause_where_combination,
    clause_order_by,
)

# processing data
from geoformat_lib.processing.data.field_statistics import field_statistics

# geoformat driver
from geoformat_lib.driver.geojson_to_geoformat import geojson_to_geolayer
from geoformat_lib.driver.geoformat_to_postgresql import geolayer_to_postgres

__version__ = 20210314


def version(version_value=__version__, verbose=True):
    version_dev = 'Alpha'
    if verbose:
        return '{version_dev} version {version_number}'.format(version_dev=version_dev, version_number=version_value)
    else:
        return version_value

####
#
# TOOLS
#
###
def point_on_segment_range(segment, step_distance, offset_distance=None):
    """
    Iterator send point coordinates on a segment at a given step distance.
    optional: add an offset distance (perpendicular to line_parameters value)

    :param segment:
    :param step_distance:
    :param offset_distance:
    :return:
    """
    start_point, end_point = segment
    native_step_distance = step_distance
    line_parameter = line_parameters((start_point, end_point))
    # test because direction of the linestring can be different from the direction of an affine line
    if euclidean_distance(start_point,
                          point_at_distance_with_line_parameters(end_point, line_parameter, step_distance,
                                                                 offset_distance=offset_distance)) < euclidean_distance(
        start_point, end_point):
        step_distance = -step_distance

    distance = euclidean_distance(start_point, end_point)

    while distance > native_step_distance:
        start_point = point_at_distance_with_line_parameters(start_point, line_parameter, step_distance,
                                                             offset_distance=offset_distance)
        yield start_point
        distance = euclidean_distance(start_point, end_point)


def points_on_linestring_distance(linestring, step_distance, offset_distance=None):
    """
    Return a point geometry that is a point on a given linestring at a given step_distance
    optional: add an offset distance (perpendicular to line_parameters value)

    :param linestring: LineString or MultiLineString geometrie
    :param step_distance: distance between each steps
    :param offset_distance: if you want you can add an offset to final on point value
    :return: Point geometrie
    """

    def points_on_linestring_part(coordinates, step_distance, offset_distance=None):

        # note about remaining_distance
        # remaining_distance is the distance that remain after a new vertex (because when there is a new vertex we have
        # to recompute the step_distance remaining

        # loop on each coordinate
        for i_point, point in enumerate(coordinates):
            if i_point == 0:
                previous_point = point
                # init remaining distance
                remaining_distance = 0
            else:
                remaining_step_distance = step_distance - remaining_distance
                segment = (previous_point, point)

                # yield first point
                if i_point == 1:
                    if offset_distance:
                        line_parameter = line_parameters(segment)
                        perp_parameter = perpendicular_line_parameters_at_point(line_parameter, previous_point)
                        first_point = point_at_distance_with_line_parameters(previous_point, perp_parameter,
                                                                             distance=offset_distance)
                        yield {'type': 'Point', 'coordinates': list(first_point)}
                    else:
                        yield {'type': 'Point', 'coordinates': list(previous_point)}

                # for just one iteration
                for new_point in point_on_segment_range(segment, remaining_step_distance, offset_distance=None):
                    remaining_distance = 0
                    # reinit values
                    previous_point = new_point
                    segment = (previous_point, point)
                    # here we cannot use offset_distance directly in point_on_segment_range used above because we have
                    # to keep initial segment direction. Then we recompute offset new_point.
                    if offset_distance:
                        line_parameter = line_parameters(segment)
                        perp_parameter = perpendicular_line_parameters_at_point(line_parameter, new_point)
                        new_point = point_at_distance_with_line_parameters(new_point, perp_parameter,
                                                                           distance=offset_distance)
                    yield {'type': 'Point', 'coordinates': list(new_point)}
                    break  # just one iteration

                # pass_on_loop check if we iterate on loop below
                pass_on_loop = False
                for new_point in point_on_segment_range(segment, step_distance, offset_distance=None):
                    remaining_distance = euclidean_distance(new_point, point)
                    pass_on_loop = True
                    # here we cannot use offset_distance directly in point_on_segment_range used above because we have
                    # to calculate the remain distance on non offseted point before. Then we recompute offset new_point
                    if offset_distance:
                        line_parameter = line_parameters(segment)
                        perp_parameter = perpendicular_line_parameters_at_point(line_parameter, new_point)
                        new_point = point_at_distance_with_line_parameters(new_point, perp_parameter,
                                                                           distance=offset_distance)
                    yield {'type': 'Point', 'coordinates': list(new_point)}

                # if no iteration en loop above we recalculate remaining distance for next point on coordinates
                if not pass_on_loop:
                    remaining_distance += euclidean_distance(point, previous_point)

                previous_point = point

    # force coordinates to MULTI
    coordinates = linestring['coordinates']
    if 'MULTI' not in linestring['type'].upper():
        coordinates = [coordinates]

    for linestring_part in coordinates:
        for point in points_on_linestring_part(linestring_part, step_distance, offset_distance=offset_distance):
            yield point


def create_pk(geolayer, pk_field_name):
    """
    'create_pk' est un dictionnaire qui permet de faire le lien entre les itérateurs features et la valeur d'un champ.

    :param geolayer: la layer au géoformat
    :param pk_field_name: le nom du champs à "indexer"
    :return: géolayer avec une contrainte de pk avce la clé du champs rajouté
    """
    # création du dictionnaire vide
    pk_dico = {}

    # récupération de la value du champs à indexer
    for i_feat in geolayer['features']:
        feature = geolayer['features'][i_feat]

        # if feature is serialized
        if 'feature_serialize' in geolayer['metadata']:
            if geolayer['metadata']['feature_serialize']:
                feature = eval(feature)

        pk_field_value = feature['attributes'][pk_field_name]
        # vérification que les valeurs sont uniques
        if pk_field_value in pk_dico:
            sys.exit('le champ indiqué contient des valeurs non unique')
        else:
            # récupération de la valeur de l'itérateur
            pk_dico[pk_field_value] = i_feat

    # affectation du dictionnaire dans les métadonnées de la géolayer
    # geolayer['metadata']['constraints'] = {'pk': {}}
    # geolayer['metadata']['constraints']['pk'][pk_field_name] = pk_dico

    return pk_dico


def pairwise(iterable):
    """
    from https://stackoverflow.com/questions/5764782/iterate-through-pairs-of-items-in-a-python-list?lq=1
    iterable = [s0, s1, s2, s3, ...]
    return ((s0,s1), (s1,s2), (s2, s3), ...)

    """
    import itertools

    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def len_coordinates(coordinates):
    """
    Return number of coordinates on a coordinates list
    """

    coordinates_count = 0
    for point in coordinates_to_point(coordinates):
        coordinates_count += 1

    return coordinates_count


def len_coordinates_in_geometry(geometry):
    """
    Return number of coordinates on a given geometry
    """
    geometry_collection = geometry_to_geometry_collection(geometry)
    coordinates_count = 0
    for geometry in geometry_collection['geometries']:
        coordinates_count += len_coordinates(geometry['coordinates'])

    return coordinates_count


def get_geocontainer_extent(geocontainer):
    if 'metadata' in geocontainer.keys():
        if 'extent' in geocontainer['metadata']:
            return geocontainer['metadata']['extent']
    else:
        for i_layer, geolayer in enumerate(geocontainer['layers']):
            geolayer_bbox = None
            if 'geometry_ref' in geolayer['metadata']:
                if 'extent' in geolayer['metadata']['geometry_ref']:
                    geolayer_bbox = geolayer['metadata']['geometry_ref']['extent']
            else:
                # no geometry in geolayer
                return None

            if not geolayer_bbox:
                for i_feat in geolayer['features']:
                    feature_bbox = None
                    if 'geometry' in geolayer['features'][i_feat].keys():
                        if 'bbox' in geolayer['features'][i_feat]['geometry']:
                            feature_bbox = geolayer['features'][i_feat]['geometry']['bbox']

                        else:
                            feature_bbox = coordinates_to_bbox(geolayer['features'][i_feat]['geometry'])
                    else:
                        # no geometry in geolayer
                        return None

                    if i_feat == 0:
                        geolayer_bbox = feature_bbox
                    else:
                        geolayer_bbox = bbox_union(geolayer_bbox, feature_bbox)

            if i_layer == 0:
                geocontainer_extent = geolayer_bbox
            else:
                geocontainer_extent = bbox_union(geocontainer_extent, geolayer_bbox)

    return geocontainer_extent


def coordinates_to_centroid(coordinates, precision=None):
    """
    Return the centroid of given coordinates list or tuple

    :param coordinates: (list or tuple) coordinates list or tuple
    :param precision: (int) precision of coordinates (number of decimal places)
    :return: (tuple) centroid
    """

    for i_point, point in enumerate(coordinates_to_point(coordinates)):
        if i_point == 0:
            mean_point = list(point)
        else:
            mean_point[0] += point[0]
            mean_point[1] += point[1]

    nb_coordinates = i_point + 1
    centroid = (mean_point[0] / nb_coordinates, mean_point[1] / nb_coordinates)
    if precision:
        centroid = (round(centroid[0], precision), round(centroid[1], precision))

    return centroid


