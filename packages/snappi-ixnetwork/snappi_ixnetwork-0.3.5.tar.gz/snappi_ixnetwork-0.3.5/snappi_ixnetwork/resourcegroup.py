import re
from snappi_ixnetwork.vport import Vport

class ResourceGroup(object):
    """"""
    def __init__(self, ixnetworkapi):
        self._api = ixnetworkapi
        self._store_properties = []
        self._layer1_conf = None
        self.layer1_check = []
        self._layer1_backup = None
        
    def set_group(self):
        self.layer1_check = []
        self._store_properties = []
        self._layer1_conf = self._api.snappi_config.layer1
        if self._layer1_conf is None or len(
                self._layer1_conf ) == 0 or self._is_redundant is True:
            return self.layer1_check

        chassis_list = self._process_property()
        response = None
        try:
            payload = {"arg1": "/availableHardware", "arg2" : []}
            url = '%s/availableHardware/operations/getChassisWithDetailedResouceGroupsInfo' \
                  % self._api._ixnetwork.href
            response = self._api._request('POST', url, payload)
        except Exception:
            raise Exception("Not able to fetch chassis details. Unable to execute L1 setting")
        chassis_id = 1
        for result in response['result']:
            chassis_dns = result["dns"]
            if chassis_dns in chassis_list:
                    self._process_groups(result['cards'],
                                     chassis_dns,
                                     chassis_id)
            chassis_id += 1
        
        final_arg2 = []
        error_ports = []
        convert_msgs = []
        idle_msgs = []
        ixn_href = self._api._ixnetwork.href
        for property in self._store_properties:
            # We will change those speed from L1 setting
            if property.aggregate is False:
                continue
            if property.group_mode is None:
                error_ports.append(property.port_name)
                continue
            args = [arg['arg1'] for arg in final_arg2]
            url = property.get_url(ixn_href)
            if url is None:
                idle_msgs.append((property.port_name,
                                  property.group_mode))
                continue
            if url not in args:
                convert_msgs.append((property.port_name,
                                     property.group_mode))
                arg2 = {
                    "arg1" : url,
                    "arg2" : property.group_mode
                }
                final_arg2.append(arg2)
        
        if len(error_ports) > 0:
            raise Exception("Please check the speed of these ports ",
                            error_ports)
        if len(idle_msgs) > 0:
            self._api.info("Speed conversion is not require for "
                           "(port.name, speed) : {0}".format(idle_msgs))
        if len(final_arg2) > 0:
            url = "{0}/availableHardware/operations/" \
                  "setresourcegroupsinfo".format(ixn_href)
            payload = {
                "arg1": "/availableHardware",
                "arg2": final_arg2,
                "arg3": True,
                "arg4": True
            }
            try:
                self._api.info("Setting (port.name, speed) : {0}".format(
                            convert_msgs))
                self._api.info(final_arg2)
                self._api._request('POST', url, payload)
            except:
                # todo: redirect to unknown page. Probable IxNetwork issue
                pass
        
        return self.layer1_check

    @property
    def _is_redundant(self):
        is_redundant = False
        if self._layer1_backup is not None:
            if self._layer1_conf == self._layer1_backup:
                self._api.info("Speed change not require "
                               "due to redundant Layer1 config")
                is_redundant = True
                for layer1 in self._layer1_conf:
                    self.layer1_check.append(layer1.name)
        self._layer1_backup = self._layer1_conf
        return is_redundant
        
    def _process_property(self):
        chassis_list = []
        port_list = []
        ports = self._api.snappi_config.ports
        for layer1 in self._layer1_conf:
            if layer1.port_names is None or len(
                    layer1.port_names) == 0:
                return
            for port in ports:
                if port in port_list:
                    return
                if port.name in layer1.port_names:
                    location = port.location
                    if location is None:
                        raise Exception("Please configure location to change speed")
                    location_info = self._api.parse_location_info(location)
                    chassis_info = location_info.chassis_info
                    if chassis_info not in chassis_list:
                        chassis_list.append(chassis_info)
                    property = StoreProperty(chassis_info,
                                        location_info.card_info,
                                        location_info.port_info,
                                        port.name,
                                        layer1)
                    self._store_properties.append(
                            property)
        return chassis_list
                    
    def _get_property(self, display_name):
        for property in self._store_properties:
            if property.port == display_name:
                return property
        return None
    
    def _process_groups(self, cards, chassis_dns, chassis_id):
        for card in cards:
            if card['cardAggregationMode'] == 'notSupported':
                continue
            if self._set_aggregate(chassis_dns, card[
                    'cardId']) is False:
                continue
            for supported_group in card['supportedGroups']:
                group_id = supported_group['id']
                current_mode = supported_group['currentSetting'][
                        'resourceGroupMode']
                for available_setting in supported_group[
                        'availableSettings']:
                    group_mode = available_setting[
                            'resourceGroupMode']
                    for panel_info in available_setting[
                            'panelInfo']:
                        for display_name in panel_info[
                                'activePortsDisplayNames']:
                            property = self._get_property(display_name)
                            if property is not None:
                                l1_name = property.set_property(chassis_id,
                                                      card,
                                                      group_id,
                                                      current_mode,
                                                      group_mode)
                                if l1_name is not None \
                                        and l1_name not in self.layer1_check:
                                    self.layer1_check.append(l1_name)
    
    def _set_aggregate(self, chassis_dns, card_id):
        fellow_card = False
        for property in self._store_properties:
            if property.chassis_dns == chassis_dns:
                if int(property.card) == 0:
                    fellow_card = True
                    property.aggregate = True
                elif int(property.card) == int(card_id):
                    fellow_card = True
                    property.aggregate = True
        return fellow_card
            
class StoreProperty(object):
    def __init__(self, chassis, card, port, port_name, layer1):
        self._chassis = chassis
        self._card = card
        self._port = port
        self._port_name = port_name
        self._speed = layer1.speed
        self._l1name = layer1.name
        self._chassis_id = None
        self._card_id = None
        self._group_id = None
        self._current_mode = None
        self._group_mode = None
        self._aggregate = False

    @property
    def chassis_dns(self):
        return self._chassis

    @property
    def card(self):
        return self._card
    
    @property
    def port(self):
        return self._port
    
    @property
    def group_mode(self):
        return self._group_mode
    
    @property
    def port_name(self):
        return self._port_name
    
    @property
    def l1name(self):
        return self._l1name
    
    @property
    def aggregate(self):
        return self._aggregate

    @aggregate.setter
    def aggregate(self, value):
        self._aggregate = value
        
    def _get_speed_map(self, card):
        """This check for specific card"""
        if re.search('maz-xb16', card[
                'appId'].lower()) is not None:
            map_speed = 'normal'
        else:
            try:
                map_speed = Vport._SPEED_MODE_MAP[
                        self._speed]
            except Exception:
                raise Exception("Speed %s not available within internal map" %
                                self._speed)
        return map_speed
    
    def set_property(self, chassis_id, card, group_id, current_mode, group_mode):
        map_speed = self._get_speed_map(card)
        if re.search(map_speed, group_mode.lower()) \
                is not None:
            self._chassis_id = chassis_id
            self._card_id = card['cardId']
            self._group_id = group_id
            self._current_mode = current_mode
            self._group_mode = group_mode
            return self._l1name
        return None
    
    def get_url(self, ixn_href):
        if self._current_mode == self._group_mode:
            return None
        url = "{0}/availableHardware/chassis/{1}" \
              "/card/{2}/aggregation/{3}".format(ixn_href,
                             self._chassis_id,
                             self._card_id,
                             self._group_id)
        return url