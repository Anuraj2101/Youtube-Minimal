targetScope = 'subscription'

param region string = 'canadaeast'

param resourceGroupName string = 'yt-minimal-dev'
param storageName string = 'storage${uniqueString(resourceGroupName)}'

resource newRG 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: region
}

module vNet './vnet.bicep' = {
  name: 'vNetModule'
  scope: newRG
  params: {
    location: newRG.location
  }
}

module storageAcct './storage.bicep' = {
  name: 'storageModule'
  scope: newRG
  params: {
    storageName: storageName
    storageLocation: newRG.location
    vNetId: vNet.outputs.virtualNetworkId
    subnetPrivateEndpointId: vNet.outputs.subnetPrivateEndpointId
    subnetPrivateEndpointName: vNet.outputs.subnetPrivateEndpointName
  }
}
