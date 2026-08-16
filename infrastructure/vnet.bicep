param location string

var virtualNetworkName = 'function-vnet'
var subnetOutbound = 'subnet-outbound'
var subnetInbound = 'subnet-inbound'
var subnetServices = 'subnet-services'

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2025-07-01' = {
  name: virtualNetworkName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
  }
  resource subnet1 'subnets' = {
    name: subnetOutbound
    properties: {
      addressPrefix: '10.0.0.0/24'
    }
  }
  resource subnet2 'subnets' = {
    name: subnetInbound
    properties: {
      addressPrefix: '10.0.1.0/24'
    }
  }
  resource subnet3 'subnets' = {
    name: subnetServices
    properties: {
      addressPrefix: '10.0.2.0/24'
    }
  }
}

output virtualNetworkId string = virtualNetwork.id
output subnetPrivateEndpointId string = resourceId('Microsoft.Network/virtualNetworks/subnets', virtualNetworkName, subnetServices)
output subnetPrivateEndpointName string = subnetServices
