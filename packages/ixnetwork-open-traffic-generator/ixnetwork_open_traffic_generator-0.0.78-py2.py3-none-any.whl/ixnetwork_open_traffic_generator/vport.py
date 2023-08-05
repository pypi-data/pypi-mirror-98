import json
import time
import re
from ixnetwork_open_traffic_generator.timer import Timer


class Vport(object):
    """Transforms OpenAPI objects into IxNetwork objects

    Args
    ----
    - ixnetworkapi (IxNetworkApi): instance of the IxNetworkApi class

    Transformations
    ---------------
    - /components/schemas/Port to /vport
    - /components/schemas/Capture to /vport/capture
    - /components/schemas/Layer1 to /vport/l1Config/...

    Process
    -------
    - Remove any vports that are not in the config.ports
    - Add any vports that are in the config.ports
    - If the location of the config.ports.location is different than the
      the /vport -connectedTo property set it to None
    - If the config.ports.location is None don't connect the ports
      else connect the port, get the vport type, set the card mode based on the
      config.layer1.speed

    Notes
    -----
    - Uses resourcemanager to set the vport location and l1Config as it is the
      most efficient way. DO NOT use the AssignPorts API as it is too slow. 
    - Only setup l1Config if location is connected. 
    - Given a connected location and speed the vport -type, card resource mode
      and l1Config sub node are derived.

    """
    _SPEED_MAP = {
        'speed_100_gbps': 'speed100g',
        'speed_50_gbps': 'speed50g',
        'speed_40_gbps': 'speed40g',
        'speed_25_gbps': 'speed25g',
        'speed_10_gbps': 'speed10g',
        'speed_1_gbps': 'speed1000',
        'speed_100_fd_mbps': 'speed100fd',
        'speed_100_hd_mbps': 'speed100hd',
        'speed_10_fd_mbps': 'speed10fd',
        'speed_10_hd_mbps': 'speed10hd'
    }
    _VM_SPEED_MAP = {
        'speed_400_gbps': 'speed400g',
        'speed_200_gbps': 'speed200g',
        'speed_100_gbps': 'speed100g',
        'speed_90_gbps': 'speed90g',
        'speed_80_gbps': 'speed80g',
        'speed_70_gbps': 'speed70g',
        'speed_60_gbps': 'speed60g',
        'speed_50_gbps': 'speed50g',
        'speed_40_gbps': 'speed40g',
        'speed_30_gbps': 'speed30g',
        'speed_25_gbps': 'speed25g',
        'speed_20_gbps': 'speed20g',
        'speed_10_gbps': 'speed10g',
        'speed_9_gbps': 'speed9000',
        'speed_8_gbps': 'speed8000',
        'speed_7_gbps': 'speed7000',
        'speed_6_gbps': 'speed6000',
        'speed_5_gbps': 'speed5000',
        'speed_4_gbps': 'speed4000',
        'speed_3_gbps': 'speed3000',
        'speed_2_gbps': 'speed2000',
        'speed_1_gbps': 'speed1000',
        'speed_100_mbps': 'speed100',
        'speed_100_fd_mbps': 'speed100',
        'speed_100_hd_mbps': 'speed100',
        'speed_10_fd_mbps': 'speed100',
        'speed_10_hd_mbps': 'speed100'
    }

    _SPEED_MODE_MAP = {
        'speed_1_gbps': 'normal',
        'speed_10_gbps': 'tengig',
        'speed_25_gbps': 'twentyfivegig',
        'speed_40_gbps': 'fortygig',
        'speed_50_gbps': 'fiftygig',
        'speed_100_gbps':
            '^(?!.*(twohundredgig|fourhundredgig)).*hundredgig.*$',
        'speed_200_gbps': 'twohundredgig',
        'speed_400_gbps': 'fourhundredgig'
    }
    
    _ADVERTISE_MAP = {
        'advertise_one_thousand_mbps': 'speed1000',
        'advertise_one_hundred_fd_mbps': 'speed100fd',
        'advertise_one_hundred_hd_mbps': 'speed100hd',
        'advertise_ten_fd_mbps': 'speed10fd',
        'advertise_ten_hd_mbps': 'speed10hd'
    }
    _FLOW_CONTROL_MAP = {
        'ieee_802_1qbb': 'ieee802.1Qbb',
        'ieee_802_3x': 'ieee802.3x'
    }

    _RESULT_COLUMNS = [
        ('frames_tx', 'Frames Tx.', int),
        ('frames_rx', 'Valid Frames Rx.', int),
        ('frames_tx_rate', 'Frames Tx. Rate', float),
        ('frames_rx_rate', 'Valid Frames Rx. Rate', float),
        ('bytes_tx', 'Bytes Tx.', int),
        ('bytes_rx', 'Bytes Rx.', int),
        ('bytes_tx_rate', 'Bytes Tx. Rate', float),
        ('bytes_rx_rate', 'Bytes Rx. Rate', float),
        ('pfc_class_0_frames_rx', 'Rx Pause Priority Group 0 Frames', int),
        ('pfc_class_1_frames_rx', 'Rx Pause Priority Group 1 Frames', int),
        ('pfc_class_2_frames_rx', 'Rx Pause Priority Group 2 Frames', int),
        ('pfc_class_3_frames_rx', 'Rx Pause Priority Group 3 Frames', int),
        ('pfc_class_4_frames_rx', 'Rx Pause Priority Group 4 Frames', int),
        ('pfc_class_5_frames_rx', 'Rx Pause Priority Group 5 Frames', int),
        ('pfc_class_6_frames_rx', 'Rx Pause Priority Group 6 Frames', int),
        ('pfc_class_7_frames_rx', 'Rx Pause Priority Group 7 Frames', int),
    ]

    def __init__(self, ixnetworkapi):
        self._api = ixnetworkapi

    def config(self):
        """Transform config.ports into Ixnetwork.Vport
        1) delete any vport that is not part of the config
        2) create a vport for every config.ports[] not present in IxNetwork
        3) set config.ports[].location to /vport -location or -connectedTo
        4) set /vport/l1Config/... properties using the corrected /vport -type
        5) connectPorts to use new l1Config settings and clearownership
        """
        self._resource_manager = self._api._ixnetwork.ResourceManager
        self._ixn_vport = self._api._vport
        with Timer(self._api, 'Ports configuration'):
            self._delete_vports()
            self._create_vports()
        with Timer(self._api, 'Captures configuration'):
            self._create_capture()
        with Timer(self._api, 'Location configuration'):
            self._set_location()
        with Timer(self._api, 'Layer1 configuration'):
            self._set_layer1()

    def _import(self, imports):
        if len(imports) > 0:
            errata = self._resource_manager.ImportConfig(
                json.dumps(imports), False)
            for item in errata:
                self._api.warning(item)
            return len(errata) == 0
        return True

    def _delete_vports(self):
        """Delete any vports from the api server that do not exist in the new config
        """
        self._api._remove(self._ixn_vport, self._api.config.ports)

    def _create_vports(self):
        """Add any vports to the api server that do not already exist
        """
        vports = self._api.select_vports()
        imports = []
        for port in self._api.config.ports:
            if port.name not in vports.keys():
                index = len(vports) + len(imports) + 1
                vport_import = {
                    'xpath': '/vport[%i]' % index,
                    'name': port.name,
                    'rxMode': 'captureAndMeasure',
                    'txMode': 'interleaved'
                }
                location = getattr(port, 'location', None)
                if location is None:
                    vport_import['connectedTo'] = location
                    port.location = None
                imports.append(vport_import)
        self._import(imports)
        for name, vport in self._api.select_vports().items():
            self._api.ixn_objects[name] = vport['href']

    def _create_capture(self):
        """Overwrite any capture settings
        """
        if self._api.config.captures is None:
            self._api.config.captures = []
        imports = []
        vports = self._api.select_vports()
        for vport in vports.values():
            if vport['capture']['hardwareEnabled'] is True or vport['capture'][
                    'softwareEnabled'] is True:
                capture = {
                    'xpath': vport['capture']['xpath'],
                    'captureMode': 'captureTriggerMode',
                    'hardwareEnabled': False,
                    'softwareEnabled': False
                }
                imports.append(capture)
        for capture_item in self._api.config.captures:
            for port_name in capture_item.port_names:
                capture_mode = 'captureTriggerMode'
                if capture_item.overwrite:
                    capture_mode = 'captureContinuousMode'
                    reset = {'xpath': vports[port_name]['xpath'] + '/capture/trigger'}
                    reset['captureTriggerEnable'] = False
                    self._import(reset)
                isEnable = False
                if capture_item.enable is True:
                    isEnable = True
                capture = {
                    'xpath': vports[port_name]['xpath'] + '/capture',
                    'captureMode': capture_mode,
                    'hardwareEnabled': isEnable,
                    'softwareEnabled': False
                }
                pallette = {'xpath': capture['xpath'] + '/filterPallette'}
                filter = {'xpath': capture['xpath'] + '/filter'}
                trigger = {'xpath': capture['xpath'] + '/trigger'}
                if capture_item.basic is not None and len(
                        capture_item.basic) > 0:
                    filter['captureFilterEnable'] = True
                    trigger['captureTriggerEnable'] = True
                    filter['captureFilterEnable'] = True
                    for basic in capture_item.basic:
                        if basic.choice == 'mac_address' and basic.mac_address.mac == 'source':
                            pallette['SA1'] = basic.mac_address.filter
                            pallette['SAMask1'] = basic.mac_address.mask
                            filter[
                                'captureFilterSA'] = 'notAddr1' if basic.not_operator is True else 'addr1'
                            trigger['triggerFilterSA'] = filter[
                                'captureFilterSA']
                        elif basic.choice == 'mac_address' and basic.mac_address.mac == 'destination':
                            pallette['DA1'] = basic.mac_address.filter
                            pallette['DAMask1'] = basic.mac_address.mask
                            filter[
                                'captureFilterDA'] = 'notAddr1' if basic.not_operator is True else 'addr1'
                            trigger['triggerFilterDA'] = filter[
                                'captureFilterDA']
                        elif basic.choice == 'custom':
                            pallette['pattern1'] = basic.custom.filter
                            pallette['patternMask1'] = basic.custom.mask
                            pallette['patternOffset1'] = basic.custom.offset
                            filter[
                                'captureFilterPattern'] = 'notPattern1' if basic.not_operator is True else 'pattern1'
                            trigger['triggerFilterPattern'] = filter[
                                'captureFilterPattern']
                imports.append(capture)
                imports.append(pallette)
                imports.append(filter)
                imports.append(trigger)
        self._import(imports)

    def _add_hosts(self, HostReadyTimeout):
        chassis = self._api._ixnetwork.AvailableHardware.Chassis
        add_addresses = []
        check_addresses = []
        for port in self._api.config.ports:
            location = getattr(port, 'location', None)
            if location is not None and ';' in location:
                chassis_address = location.split(';')[0]
                chassis.find(Hostname='^%s$' % chassis_address)
                if len(chassis) == 0:
                    add_addresses.append(chassis_address)
                check_addresses.append(chassis_address)
        add_addresses = set(add_addresses)
        check_addresses = set(check_addresses)
        if len(add_addresses) > 0:
            with Timer(self._api,
                       'Add location hosts [%s]' % ', '.join(add_addresses)):
                for add_address in add_addresses:
                    chassis.add(Hostname=add_address)
        if len(check_addresses) > 0:
            with Timer(
                    self._api,
                    'Location hosts ready [%s]' % ', '.join(check_addresses)):
                start_time = time.time()
                while True:
                    chassis.find(Hostname='^(%s)$' % '|'.join(check_addresses),
                                 State='^ready$')
                    if len(chassis) == len(check_addresses):
                        break
                    if time.time() - start_time > HostReadyTimeout:
                        raise RuntimeError(
                            'After %s seconds, not all location hosts [%s] are reachable'
                            % (HostReadyTimeout, ', '.join(check_addresses)))
                    time.sleep(2)

    def _get_layer1(self, port):
        if hasattr(self._api.config, 'layer1') is False:
            return
        if len(self._api.config.layer1) == 0:
            return
        for layer1 in self._api.config.layer1:
            for port_names in layer1.port_names:
                if port.name in port_names:
                    return layer1
        
    def _set_aggregation(self, port, imports):
        """ If the card has multiple resource group to control speed within port
        set it according to the speed"""

        resource_group = None
        location = getattr(port, 'location', None)
        if location is None or len(location) == 0:
            return
        
        (hostname, cardid, portid) = location.split(';')
        layer1 = self._get_layer1(port)
        if layer1 is None:
            return
        
        speed_mode_map = Vport._SPEED_MODE_MAP
        self._api.info("Checking port %s to set Layer1 speed %s" %
                       (port.name, layer1.speed))
        card_info = self._api.select_card_aggregation(location)
        if 'aggregation' in card_info.keys() and len(card_info[
                         'aggregation']) > 0:
            for aggregation in card_info['aggregation']:
                if portid in [res_port.split('/')[-1] for res_port in aggregation[
                        'resourcePorts']]:
                    self._reset_resource_mode(card_info, speed_mode_map)
                    resource_group = aggregation
                    break
        
        aggregation_mode = None
        if resource_group is not None:
            if layer1.speed in speed_mode_map:
                mode = speed_mode_map[layer1.speed]
                for available_mode in resource_group['availableModes']:
                    if re.search(mode, available_mode.lower()) is not None:
                        layer1.__setattr__('speed_taken_care', True)
                        aggregation_mode = available_mode
                        break
            else:
                self._api.warning("Speed %s not avialable within internal map" %
                                  layer1.speed)
        else:
            self._api.warning("Please check physical port number for port %s" %
                              port.name)

        if aggregation_mode is not None:
            if aggregation_mode != resource_group['mode']:
                imports.append({
                    'xpath': resource_group['xpath'],
                    'mode': aggregation_mode
                })
    
                self._api.info('Setting port %s to resource mode %s' %
                               (port.name, aggregation_mode))
            else:
                self._api.info("Port %s already set to resource mode %s" %
                               (port.name, aggregation_mode))
        else:
            self._api.warning("Speed %s not available within RG of port %s" %
                              (layer1.speed, port.name))
            
    
    def _set_location(self):
        location_supported = True
        try:
            self._api._ixnetwork._connection._options(
                self._api._ixnetwork.href + '/locations')
        except Exception:
            location_supported = False
        
        self._add_hosts(60)
        
        # calling little bit costly operation? Otherwise we can't handle same port config for
        # multiple run (_set_card_resource_mode reset to card level). Also some ports are
        # handling multiple speed ('novusFourByTwentyFiveGigNonFanOut' and 'novusFourByTenGigNonFanOut')
        imports = []
        with Timer(self._api,
                   'Aggregation mode speed change'):
            for port in self._api.config.ports:
                self._set_aggregation(port, imports)
            if self._import(imports) is False:
                self._api.info('Retrying card resource mode change')
                self._import(imports)
                
        vports = self._api.select_vports()
        locations = []
        imports = []
        clear_locations = []
        for port in self._api.config.ports:
            vport = vports[port.name]
            location = getattr(port, 'location', None)

            if location_supported is True:
                if vport['location'] == location and vport[
                        'connectionState'].startswith('connectedLink'):
                    continue
            else:
                if len(vport['connectedTo']) > 0 and vport[
                        'connectionState'].startswith('connectedLink'):
                    continue
                    
            self._api.ixn_objects[port.name] = vport['href']
            vport = {'xpath': vports[port.name]['xpath']}
            if location_supported is True:
                vport['location'] = location
            else:
                if location is not None:
                    xpath = self._api.select_chassis_card_port(location)
                    vport['connectedTo'] = xpath
                else:
                    vport['connectedTo'] = ''
            imports.append(vport)
            if location is not None and len(location) > 0:
                clear_locations.append(location)
                locations.append(port.name)
        if len(locations) == 0:
            return
        self._clear_ownership(clear_locations)
        with Timer(self._api, 'Location connect [%s]' % ', '.join(locations)):
            self._import(imports)
        with Timer(self._api,
                   'Location state check [%s]' % ', '.join(locations)):
            self._api._vport.find(ConnectionState='^(?!connectedLink).*$')
            if len(self._api._vport) > 0:
                self._api._vport.ConnectPorts()
            start = time.time()
            timeout = 10
            while True:
                self._api._vport.find(Name='^(%s)$' % '|'.join(locations),
                                      ConnectionState='^connectedLink')
                if len(self._api._vport) == len(locations):
                    break
                if time.time() - start > timeout:
                    unreachable = []
                    self._api._vport.find(ConnectionState='^(?!connectedLink).*$')
                    for vport in self._api._vport:
                        unreachable.append('%s [%s: %s]' % (vport.Name, vport.ConnectionState, vport.ConnectionStatus))
                    raise RuntimeError(
                        'After %s seconds, %s are unreachable' % (timeout, ', '.join(unreachable)))
                time.sleep(2)
            for vport in self._api._vport.find(
                    ConnectionState='^(?!connectedLinkUp).*$'):
                self._api.warning('%s %s' %
                                  (vport.Name, vport.ConnectionState))

    def _set_layer1(self):
        """Set the /vport/l1Config/... properties
        This should only happen if the vport connectionState is connectedLink...
        as it determines the ./l1Config child node.
        """
        if hasattr(self._api.config, 'layer1') is False:
            return
        if self._api.config.layer1 is None:
            return
        reset_auto_negotiation = dict()
        # set and commit the card resource mode
        vports = self._api.select_vports()
        imports = []
        for layer1 in self._api.config.layer1:
            for port_name in layer1.port_names:
                self._set_card_resource_mode(vports[port_name], layer1,
                                             imports)
        if self._import(imports) is False:
            # WARNING: this retry is because no reasonable answer as to why
            # changing card mode periodically fails with this opaque message
            # 'Releasing ownership on ports failed.'
            self._api.info('Retrying card resource mode change')
            self._import(imports)
        # set the vport type
        imports = []
        for layer1 in self._api.config.layer1:
            for port_name in layer1.port_names:
                self._set_vport_type(vports[port_name], layer1, imports)
        self._import(imports)
        vports = self._api.select_vports()
        # set the remainder of l1config properties
        imports = []
        for layer1 in self._api.config.layer1:
            for port_name in layer1.port_names:
                self._set_l1config_properties(vports[port_name], layer1,
                                              imports)
        self._import(imports)
        # Due to dependency attribute (ieeeL1Defaults)
        # reset enableAutoNegotiation
        imports = []
        for layer1 in self._api.config.layer1:
            for port_name in layer1.port_names:
                vport = vports[port_name]
                if port_name in reset_auto_negotiation and reset_auto_negotiation[
                        port_name]:
                    self._reset_auto_negotiation(vport, layer1, imports)
        self._import(imports)

    def _set_l1config_properties(self, vport, layer1, imports):
        """Set vport l1config properties
        """
        if vport['connectionState'] not in [
                'connectedLinkUp', 'connectedLinkDown'
        ]:
            return
        self._set_fcoe(vport, layer1, imports)
        self._import(imports)
        
        self._set_auto_negotiation(vport, layer1, imports)

    def _reset_resource_mode(self, card, speed_mode_map):
        # add check for novus NOVUS10
        novus10g_modes = ['normal', 'tenGigAggregation']
        if re.search('novus', card['description'].lower()) and set(
                novus10g_modes) == set(card['availableModes']):
            speed_mode_map['speed_10_gbps'] = 'normal'
    
    def _set_card_resource_mode(self, vport, layer1, imports):
        """If the card has an aggregation mode set it according to the speed
        """
        if vport['connectionState'] not in [
                'connectedLinkUp', 'connectedLinkDown'
        ] or hasattr(layer1, 'speed_taken_care'):
            return

        aggregation_mode = None
        if layer1.speed in Vport._SPEED_MODE_MAP:
            card = self._api.select_chassis_card(vport)
            mode = Vport._SPEED_MODE_MAP[layer1.speed]
            for available_mode in card['availableModes']:
                if re.search(mode, available_mode.lower()) is not None:
                    aggregation_mode = available_mode
                    break
        if aggregation_mode is not None and aggregation_mode != card[
                'aggregationMode']:
            self._api.info('Setting %s to resource mode %s' %
                           (card['description'], aggregation_mode))
            imports.append({
                'xpath': card['xpath'],
                'aggregationMode': aggregation_mode
            })

    def _set_auto_negotiation(self, vport, layer1, imports):
        if layer1.speed.endswith('_mbps') or layer1.speed == 'speed_1_gbps':
            self._set_ethernet_auto_negotiation(vport, layer1, imports)
        else:
            self._set_gigabit_auto_negotiation(vport, layer1, imports)

    def _set_vport_type(self, vport, layer1, imports):
        """Set the /vport -type
        
        If flow_control is not None then the -type attribute should 
        be switched to a type with the Fcoe extension if it is allowed.

        If flow_control is None then the -type attribute should 
        be switched to a type without the Fcoe extension.
        """
        fcoe = False
        if hasattr(layer1, 'flow_control') and layer1.flow_control is not None:
            fcoe = True
        vport_type = vport['type']
        elegible_fcoe_vport_types = [
            'ethernet', 'tenGigLan', 'fortyGigLan', 'tenGigWan',
            'hundredGigLan', 'tenFortyHundredGigLan', 'novusHundredGigLan',
            'novusTenGigLan', 'krakenFourHundredGigLan',
            'aresOneFourHundredGigLan', 'starFourHundredGigLan'
        ]
        if fcoe is True and vport_type in elegible_fcoe_vport_types:
            vport_type = vport_type + 'Fcoe'
        if fcoe is False and vport_type.endswith('Fcoe'):
            vport_type = vport_type.replace('Fcoe', '')
        if vport_type != vport['type']:
            imports.append({
                'xpath': vport['xpath'] + '/l1Config',
                'currentType': vport_type
            })
        return vport_type

    def _set_ethernet_auto_negotiation(self, vport, layer1, imports):
        advertise = []
        if layer1.speed == 'speed_1_gbps':
            advertise.append(
                Vport._ADVERTISE_MAP['advertise_one_thousand_mbps'])
        if layer1.speed == 'speed_100_fd_mbps':
            advertise.append(
                Vport._ADVERTISE_MAP['advertise_one_hundred_fd_mbps'])
        if layer1.speed == 'speed_100_hd_mbps':
            advertise.append(
                Vport._ADVERTISE_MAP['advertise_one_hundred_hd_mbps'])
        if layer1.speed == 'speed_10_fd_mbps':
            advertise.append(Vport._ADVERTISE_MAP['advertise_ten_fd_mbps'])
        if layer1.speed == 'speed_10_hd_mbps':
            advertise.append(Vport._ADVERTISE_MAP['advertise_ten_hd_mbps'])
        proposed_import = {
            'xpath':
            vport['xpath'] + '/l1Config/' + vport['type'].replace('Fcoe', ''),
            'speed':
            self._get_speed(vport, layer1),
            'media':
            layer1.media,
            'autoNegotiate':
            layer1.auto_negotiate,
            'speedAuto':
            advertise
        }
        self._add_l1config_import(vport, proposed_import, imports)

    def _add_l1config_import(self, vport, proposed_import, imports):
        type = vport['type'].replace('Fcoe', '')
        l1config = vport['l1Config'][type]
        key_to_remove = []
        for key in proposed_import:
            if key == 'xpath':
                continue
            if key not in l1config or l1config[key] == proposed_import[key]:
                key_to_remove.append(key)
        # add this constrain due to handle some specific use case (1G to 10G)
        if 'speed' in key_to_remove and 'speedAuto' not in key_to_remove:
            key_to_remove.remove('speed')
        for key in key_to_remove:
            proposed_import.pop(key)
        if len(proposed_import) > 0:
            imports.append(proposed_import)

    def _set_gigabit_auto_negotiation(self, vport, layer1, imports):
        advertise = []
        advertise.append(Vport._SPEED_MAP[layer1.speed])
        auto_field_name  = 'enableAutoNegotiation'
        if re.search('novustengiglan', vport['type'].lower()) is not None:
            auto_field_name = 'autoNegotiate'
        proposed_import = {
            'xpath':
            vport['xpath'] + '/l1Config/' + vport['type'].replace('Fcoe', ''),
            'ieeeL1Defaults':
            layer1.ieee_media_defaults,
            'speed':
            Vport._SPEED_MAP[layer1.speed],
            '{0}'.format(auto_field_name):
            False if layer1.auto_negotiate is None else layer1.auto_negotiate,
            'enableRsFec':
            False if layer1.auto_negotiation is None else
            layer1.auto_negotiation.rs_fec,
            'linkTraining':
            False if layer1.auto_negotiation is None else
            layer1.auto_negotiation.link_training,
            'speedAuto':
            advertise
        }
        if layer1.media is not None:
            proposed_import['media'] = layer1.media
            
        self._add_l1config_import(vport, proposed_import, imports)

    def _get_speed(self, vport, layer1):
        if vport['type'] == 'ethernetvm':
            return Vport._VM_SPEED_MAP[layer1.speed]
        else:
            return Vport._SPEED_MAP[layer1.speed]

    def _reset_auto_negotiation(self, vport, layer1, imports):
        if layer1.speed.endswith(
                '_mbps') is False and layer1.speed != 'speed_1_gbps':
            imports.append({
                'xpath':
                vport['xpath'] + '/l1Config/' +
                vport['type'].replace('Fcoe', ''),
                'enableAutoNegotiation':
                layer1.auto_negotiate,
            })

    def _set_fcoe(self, vport, layer1, imports):
        if hasattr(layer1, 'flow_control') and layer1.flow_control is None:
            return
        xpath = '%s/l1Config/%s/fcoe' % (vport['xpath'], vport['type'].replace(
            'Fcoe', ''))
        fcoe = {
            'xpath': xpath,
            'flowControlType':
            Vport._FLOW_CONTROL_MAP[layer1.flow_control.choice]
        }
        if layer1.flow_control.choice == 'ieee_802_1qbb':
            pfc = layer1.flow_control.ieee_802_1qbb
            fcoe['enablePFCPauseDelay'] = False if pfc.pfc_delay == 0 else True
            fcoe['pfcPauseDelay'] = pfc.pfc_delay
            fcoe['pfcPriorityGroups'] = [
                -1 if pfc.pfc_class_0 is None else pfc.pfc_class_0,
                -1 if pfc.pfc_class_1 is None else pfc.pfc_class_1,
                -1 if pfc.pfc_class_2 is None else pfc.pfc_class_2,
                -1 if pfc.pfc_class_3 is None else pfc.pfc_class_3,
                -1 if pfc.pfc_class_4 is None else pfc.pfc_class_4,
                -1 if pfc.pfc_class_5 is None else pfc.pfc_class_5,
                -1 if pfc.pfc_class_6 is None else pfc.pfc_class_6,
                -1 if pfc.pfc_class_7 is None else pfc.pfc_class_7,
            ]
            fcoe['priorityGroupSize'] = 'priorityGroupSize-8'
            fcoe['supportDataCenterMode'] = True
        imports.append(fcoe)

    def _clear_ownership(self, locations):
        try:
            force_ownership = self._api.config.options.port_options.location_preemption
        except Exception:
            force_ownership = False
        if force_ownership is True:
            available_hardware_hrefs = {}
            location_hrefs = {}
            for location in locations:
                if ';' in location:
                    clp = location.split(';')
                    chassis = self._api._ixnetwork.AvailableHardware.Chassis.find(
                        Hostname=clp[0])
                    if len(chassis) > 0:
                        available_hardware_hrefs[
                            location] = '%s/card/%s/port/%s' % (
                                chassis.href, abs(int(clp[1])), abs(int(
                                    clp[2])))
                elif '/' in location:
                    appliance = location.split('/')[0]
                    locations = self._api._ixnetwork.Locations
                    locations.find(Hostname=appliance)
                    if len(locations) == 0:
                        locations.add(Hostname=appliance)
                    ports = locations.Ports.find(Location='^%s$' % location)
                    if len(ports) > 0:
                        location_hrefs[location] = ports.href
            self._api.clear_ownership(available_hardware_hrefs, location_hrefs)

    def _set_result_value(self,
                          row,
                          column_name,
                          column_value,
                          column_type=str):
        if len(self._column_names
               ) > 0 and column_name not in self._column_names:
            return
        try:
            row[column_name] = column_type(column_value)
        except Exception:
            if column_type.__name__ in ['float', 'int']:
                row[column_name] = 0
            else:
                row[column_type] = column_value

    def results(self, request):
        """Return port results
        """
        if request.column_names is None:
            self._column_names = []
        else:
            self._column_names = request.column_names
        
        port_filter = {'property': 'name', 'regex': '.*'}
        port_names = [port.name for port in self._api._config.ports]
        if request and request.port_names:
            port_names = request.port_names
        if len(port_names) == 1:
            port_filter['regex'] = '^%s$' % port_names[0]
        elif len(port_names) > 1:
            port_filter['regex'] = '^(%s)$' % '|'.join(port_names)
            
        port_rows = {}
        for vport in self._api.select_vports(port_name_filters=[port_filter]).values():
            port_row = {}
            self._set_result_value(port_row, 'name', vport['name'])
            location = vport['location']
            if vport['connectionState'].startswith('connectedLink') is True:
                location += ';connected'
            elif len(location) > 0:
                location += ';' + vport['connectionState']
            else:
                location = vport['connectionState']
            self._set_result_value(port_row, 'location', location)
            self._set_result_value(
                port_row, 'link', 'up'
                if vport['connectionState'] == 'connectedLinkUp' else 'down')
            self._set_result_value(port_row, 'capture', 'stopped')
            # init all columns with corresponding zero-values so that
            # the underlying dictionary contains all requested columns
            # in an event of unwanted exceptions
            for ext_name, _, typ in self._RESULT_COLUMNS:
                self._set_result_value(port_row, ext_name, 0, typ)

            port_rows[vport['name']] = port_row

        try:
            table = self._api.assistant.StatViewAssistant('Port Statistics')
            # TBD: REMOVE unnecessary try/except
            for row in table.Rows:
                # keep plugging values for next columns even if the
                # current one raises exception
                try:
                    port_row = port_rows[row['Port Name']]
                    for ext_name, int_name, typ in self._RESULT_COLUMNS:
                        try:
                            self._set_result_value(port_row, ext_name,
                                                   row[int_name], typ)
                        except Exception:
                            # TODO print a warning maybe ?
                            pass
                except Exception:
                    # TODO print a warning maybe ?
                    pass

        except Exception:
            # TODO print a warning maybe ?
            pass

        return port_rows.values()
