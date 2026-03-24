targetScope = 'subscription'

param location string = 'canadaeast'

param resourceGroupName string = 'yt-minimal-dev'
param storageName string = 'storage${uniqueString(resourceGroupName)}'

resource newRG 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: location
}

module storageAcct './storage.bicep' = {
  name: 'storageModule'
  scope: newRG
  params: {
    storageName: storageName
    storageLocation: location
  }
}
