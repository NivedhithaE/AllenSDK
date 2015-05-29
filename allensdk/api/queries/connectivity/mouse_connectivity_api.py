# Copyright 2015 Allen Institute for Brain Science
# This file is part of Allen SDK.
#
# Allen SDK is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Allen SDK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Allen SDK.  If not, see <http://www.gnu.org/licenses/>.

from allensdk.api.api import Api
from allensdk.api.queries.rma.rma_api import RmaApi
import json

class MouseConnectivityApi(Api):
    '''HTTP Client for the Allen Mouse Brain Connectivity Atlas.
    
    See: `Mouse Connectivity API <http://help.brain-map.org/display/mouseconnectivity/API>`_
    '''
    product_id = 5
    
    def __init__(self, base_uri=None):
        super(MouseConnectivityApi, self).__init__(base_uri)
    
    
    def build_query(self, structure_id=None, fmt='json'):
        '''Build the URL that will fetch experiments 
        in the "Mouse Connectivity Projection" Product.
        
        Parameters
        ----------
        structure_id : integer, optional
            injection structure
        fmt : string, optional
            json (default) or xml
        
        Returns
        -------
        url : string
            The constructed URL
        '''
        
        if structure_id:
            structure_filter = '[id$eq%d]' % (structure_id)
        else:
            structure_filter = ''
        
        url = ''.join([self.rma_endpoint,
                       '/query.',
                       fmt,
                       '?q=',
                       'model::SectionDataSet',
                       ',rma::criteria,',
                       'products[id$eq%d]' % (MouseConnectivityApi.product_id),
                       ',rma::include,',
                       'specimen',
                       '(stereotaxic_injections',
                       '(primary_injection_structure,',
                       'structures',
                       structure_filter,
                       '))'])
        
        return url
    
    
    def build_detail_query(self, experiment_id, fmt='json'):
        '''Construct a query for detailed metadata for one experiment.
        
        Parameters
        ----------
        fmt : string, optional
            json (default) or xml
        
        Returns
        -------
        url : string
            The constructed URL
        '''
        url = ''.join([self.rma_endpoint,
                       '/query.',
                       fmt,
                       '?q=',
                       'model::SectionDataSet',
                       ',rma::criteria,',
                       '[id$eq%d]' % (experiment_id),
                       ',rma::include,',
                       'specimen',
                       '(stereotaxic_injections',
                       '(primary_injection_structure,',
                       'structures,',
                       'stereotaxic_injection_coordinates)),',
                       'equalization,',
                       'sub_images',
                       ',rma::options',
                       "[order$eq'sub_images.section_number$asc']"])
        
        return url
    
    
    def build_projection_image_meta_info(self,
                                         experiment_id,
                                         section_number,
                                         fmt='json'):
        '''Construct URL to fetch meta-information of one projection image.
        
        Parameters
        ----------
        experiment_id : integer
        section_number : integer
        fmt : string, optional
            json (default) or xml
        
        Returns
        -------
        url : string
            The constructed URL
        '''
        url = ''.join([self.rma_endpoint,
                       '/query.',
                       fmt,
                       '?q=',
                       'model::SectionDataSet',
                       ',rma::criteria,',
                       '[id$eq%d]' % (experiment_id),
                       ',rma::include,',
                       'equalization,',
                       'sub_images',
                       '[section_number$eq%d]' % (section_number)])
        
        return url
    
    
    def build_structure_projection_signal_statistics_url(self,
                                                         section_data_set_id,
                                                         is_injection=None,
                                                         fmt='json'):
        '''Query for projection signal statistics for one injection experiment.
        
        Parameters
        ----------
        section_data_set_id : integer
        is_injection : boolean, optional
        fmt : string, optional
            json (default) or xml
        
        Returns
        -------
        url : string
            The constructed URL
        
        Notes
        -----
        See: examples under `Projection Structure Unionization <http://help.brain-map.org/display/mouseconnectivity/API#API-ProjectionStructureUnionization>`_.
        
        '''
        criteria_params = [',rma::criteria,',
                           '[section_data_set_id$eq%d]' % (section_data_set_id)]
        
        if is_injection != None:
            if is_injection:
                criteria_params.append('[is_injection$eqtrue]')
            else:
                criteria_params.append('[is_injection$eqtrue]')
        
        criteria_clause = ''.join(criteria_params)
        include_clause = ''.join([',rma::include,',
                                  'structure'])
        options_clause = ''.join([',rma::options,',
                                  '[num_rows$eq5000]'])
        
        url = ''.join([self.rma_endpoint,
                       '/query.',
                       fmt,
                       '?q=',
                       'model::ProjectionStructureUnionize',
                       criteria_clause,
                       include_clause,
                       options_clause])
        
        return url
    
    
    def build_signal_statistics_url(self,
                                    section_data_set_id,
                                    is_injection=None,
                                    fmt='json'):
        '''Query for projection signal statistics for one injection experiment.
        
        Parameters
        ----------
        section_data_set_id : integer
        is_injection : boolean, optional
        fmt : string, optional
            json (default) or xml
        
        Returns
        -------
        url : string
            The constructed URL
        
        Notes
        -----
        See: examples under `Projection Structure Unionization <http://help.brain-map.org/display/mouseconnectivity/API#API-ProjectionStructureUnionization>`_.
        Setting is_injection to False will get the projection signal statistics exclusive of injection area.
        Setting is_injection to True will get the injection site statistics for the experiment.
        '''
        criteria_params = [',rma::criteria,',
                           '[section_data_set_id$eq%d]' % (section_data_set_id)]
        
        if is_injection != None:
            if is_injection:
                criteria_params.append('[is_injection$eqtrue]')
            else:
                criteria_params.append('[is_injection$eqtrue]')
        
        criteria_clause = ''.join(criteria_params)
        include_clause = ''.join([',rma::include,',
                                  'structure'])
        options_clause = ''.join([',rma::options,',
                                  '[num_rows$eq5000]'])
        
        url = ''.join([self.rma_endpoint,
                       '/query.',
                       fmt,
                       '?q=',
                       'model::ProjectionStructureUnionize',
                       criteria_clause,
                       include_clause,
                       options_clause])
    
    
    def build_projection_grid_search_url(self,
                                         injection_structures=None,
                                         target_domain=None,
                                         injection_hemisphere=None,
                                         target_hemisphere=None,
                                         transgenic_lines=None,
                                         injection_domain=None,
                                         primary_structure_only=None,
                                         start_row=None,
                                         num_rows=None,
                                         fmt='json'):
        '''Search over the whole projection signal statistics dataset
        to find experiments with specific projection profiles.
        
        Parameters
        ----------
        injection_structures : list of integers or strings
            Integer Structure.id or String Structure.acronym.
        target_domain : list of integers or strings, optional
            Integer Structure.id or String Structure.acronym.
        injection_hemisphere : string, optional
            'right' or 'left', Defaults to both hemispheres.
        target_hemisphere : string, optional
            'right' or 'left', Defaults to both hemispheres.
        transgenic_lines : list of integers or strings, optional
             Integer TransgenicLine.id or String TransgenicLine.name. Specify ID 0 to exclude all TransgenicLines.
        injection_domain : list of integers or strings, optional
             Integer Structure.id or String Structure.acronym.
        primary_structure_only : boolean, optional
        start_row : integer, optional
            For paging purposes. Defaults to 0.
        num_rows : integer, optional
            For paging purposes. Defaults to 2000.
        
        Notes
        -----
        See `Projection Grid Search Service <http://help.brain-map.org/display/mouseconnectivity/API#API-ProjectionStructureUnionization#API-ProjectionGridSearchService>`_
        and 
        `service::mouse_connectivity_injection_structure <http://help.brain-map.org/display/api/Connected+Services+and+Pipes#ConnectedServicesandPipes-service%3A%3Amouseconnectivityinjectionstructure>`_.
        
        '''
        rma = RmaApi()
        service_name = 'mouse_connectivity_injection_structure'
        
        params = [('injection_structures', injection_structures),
                  ('target_domain', target_domain),
                  ('injection_hemisphere', injection_hemisphere),
                  ('target_hemisphere', target_hemisphere),
                  ('transgenic_lines', transgenic_lines),
                  ('injection_domain', injection_domain),
                  ('primary_structure_only', primary_structure_only),
                  ('start_row', start_row),
                  ('num_rows', num_rows)]
        service_stage = rma.service_stage(service_name,
                                          params)
        url = RmaApi().build_query_url([service_stage],
                                       fmt)
        
        return url
    
    
    def read_response(self, parsed_json):
        '''Return the list of cells from the parsed query.
        
        Parameters
        ----------
        parsed_json : dict
            A python structure corresponding to the JSON data returned from the API.
        '''
        return parsed_json['msg']
    
    
    def get_experiments(self, structure_id):
        '''Retrieve the experimants data.'''
        data = self.do_query(self.build_query,
                             self.read_response,
                             structure_id)
        
        return data
    
    
    def get_experiment_detail(self, experiment_id):
        '''Retrieve the experimants data.'''
        data = self.do_query(self.build_detail_query,
                             self.read_response,
                             experiment_id)
        
        return data
    
    
    def get_projection_image_meta_info(self,
                                       experiment_id,
                                       section_number):
        '''Fetch meta-information of one projection image.
        
        Parameters
        ----------
        experiment_id : integer
        
        section_number : integer
        
        Notes
        -----
        See: image examples under 
        `Experimental Overview and Metadata <http://help.brain-map.org/display/mouseconnectivity/API##API-ExperimentalOverviewandMetadata>`_
        for additional documentation.
        Download the image using :py:meth:`allensdk.api.queries.image.image_download_api.ImageDownloadApi.download_section_image` 
        '''
        data = self.do_query(self.build_projection_image_meta_info,
                             self.read_response,
                             experiment_id,
                             section_number)
        
        return data
    
    
    def get_structure_projection_signal_statistics(self,
                                                   section_data_set_id,
                                                   is_injection=None):
        '''Fetch meta-information of one projection image.
        
        Parameters
        ----------
        experiment_id : integer
        section_number : integer
        
        Returns
        -------
        data : dict
            Parsed JSON data message.
        
        Notes
        -----
        See: examples under `Projection Structure Unionization <http://help.brain-map.org/display/mouseconnectivity/API#API-ProjectionStructureUnionization>`_.
        '''
        data = self.do_query(self.build_signal_statistics_url,
                             self.read_response,
                             section_data_set_id,
                             is_injection)
        
        return data
    
    
    def download_volumetric_data(self,
                                 data,
                                 file_name,
                                 voxel_resolution=None,
                                 save_file_path=None,
                                 release=None,
                                 coordinate_framework=None):
        '''Download 3D reference model in NRRD format.
        
        Parameters
        ----------
        data : string
            'average_template', 'ara_nissl', 'annotation/ccf_2015', 'annotation/mouse_2011', or 'annotation/devmouse_2012'
        voxel_resolution : int
            10, 25, 50 or 100
        coordinate_framework : string
            'mouse_ccf' (default) or 'mouse_annotation'
            
        Notes
        -----
        See: `3-D Reference Models <http://help.brain-map.org/display/mouseconnectivity/API#API-3DReferenceModels>`_ 
        for additional documentation.
        '''
        
        if voxel_resolution == None:
            voxel_resolution = 10
            
        if save_file_path == None:
            save_file_path = file_name
        
        if release == None:
            release = 'current-release'
        
        if coordinate_framework == None:
            coordinate_framework = 'mouse_ccf'
        
        url = ''.join([self.informatics_archive_endpoint,
                       '/%s/%s/' % (release, coordinate_framework),
                       data,
                       '/',
                       file_name])
        
        self.retrieve_file_over_http(url, save_file_path)


if __name__ == '__main__':
    import nrrd
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    a = MouseConnectivityApi()
    #print(a.build_projection_grid_search_url(injection_structures='Isocortex',
    #                                         primary_structure_only='true'))
    print(a.build_projection_grid_search_url(injection_structures='Isocortex',
                                             transgenic_lines=RmaApi().quote_string('Syt6-Cre_KI148'),
                                             primary_structure_only='true'))
    #print(json.dumps(a.get_experiments()))
    #print(json.dumps(a.get_experiments(structure_id=385)))
    #print(json.dumps(a.get_experiment_detail(experiment_id=126862385)))
    #print(json.dumps(a.get_projection_image_meta_info(experiment_id=126862385,
    #                                                  section_number=74)))
    #a.download_volumetric_data('average_template', 'average_template_25.nrrd')
    #a.download_volumetric_data('ara_nissl', 'ara_nissl_25.nrrd')
    #a.download_volumetric_data('annotation/ccf_2015', 'annotation_25.nrrd')
#     AVGT, metaAVGT = nrrd.read('average_template_25.nrrd')
#     NISSL, metaNISSL = nrrd.read('ara_nissl_25.nrrd')
#     ANO, metaANO = nrrd.read('annotation_25.nrrd')
#     
#     # Save one coronal section as PNG
#     slice = AVGT[264,:,:].astype(float)
#     slice /= np.max(slice)
#     im = Image.fromarray(np.uint8(plt.cm.gray(slice)*255))
#     im.save('output/avgt_coronal.png')
#     
#     slice = NISSL[264,:,:].astype(float)
#     slice /= np.max(slice)
#     im = Image.fromarray(np.uint8(plt.cm.gray(slice)*255))
#     im.save('output/nissl_coronal.png')
#     
#     slice = ANO[264,:,:].astype(float)
#     slice /= 2000
#     im = Image.fromarray(np.uint8(plt.cm.jet(slice)*255))
#     im.save('output/ano_coronal.png')
#     
#     # Save one sagittal section as PNG
#     slice = AVGT[:,:,220].astype(float)
#     slice /= np.max(slice)
#     im = Image.fromarray(np.uint8(plt.cm.gray(slice)*255))
#     im.save('output/avgt_sagittal.png')
#     
#     slice = NISSL[:,:,220].astype(float)
#     slice /= np.max(slice)
#     im = Image.fromarray(np.uint8(plt.cm.gray(slice)*255))
#     im.save('output/nissl_sagittal.png')
#     
#     slice = ANO[:,:,220].astype(float)
#     slice /= 2000
#     im = Image.fromarray(np.uint8(plt.cm.jet(slice)*255))
#     im.save('output/ano_sagittal.png')
