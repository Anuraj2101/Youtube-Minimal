param storageName string
param storageLocation string

resource storageAcct 'Microsoft.Storage/storageAccounts@2025-06-01' = {
  name: storageName
  location: storageLocation
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'Storage'
  properties: {}
}
