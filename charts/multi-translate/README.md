multi-translate
===============
A unified interface on top of various translate APIs providing optimal translations, caching, fallback.

Current chart version is `0.1.0`



## Chart Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://kubernetes-charts.storage.googleapis.com/ | postgresql | 8.6.4 |

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| config | object | `{"amazon":{"region":null},"deepL":{"endpoint":"https://api.deepl.com/v2/"},"google":{"endpoint":"https://translation.googleapis.com","parentPath":null},"logLevel":null,"microsoft":{"endpoint":null,"region":"global","usingVirtualNetwork":false},"papago":{"endpoint":"https://openapi.naver.com/v1/papago/n2mt","naverCloud":false},"secrets":{"awsAccessKeyId":{"key":null,"name":null},"awsSecretAccessKey":{"key":null,"name":null},"deepLAuthKey":{"key":null,"name":null},"googleServiceAccount":{"key":null,"name":null},"microsoftTranslatorSubscriptionKey":{"key":null,"name":null},"papagoClientId":{"key":null,"name":null},"papagoClientSecret":{"key":null,"name":null},"yandexIAMToken":{"key":null,"name":null}},"yandex":{"endpoint":"https://translate.api.cloud.yandex.net/translate/v2/","folderId":null}}` | Multi-Translate configuration |
| config.amazon | object | `{"region":null}` | Configuration related to amazon translate |
| config.amazon.region | string | `nil` | The aws region your amazon translate service belongs to |
| config.deepL | object | `{"endpoint":"https://api.deepl.com/v2/"}` | Configuration related to the Deep L Translation service |
| config.deepL.endpoint | string | `"https://api.deepl.com/v2/"` | The deepL HTTP endpoint |
| config.google | object | `{"endpoint":"https://translation.googleapis.com","parentPath":null}` | Configuration related to google translate |
| config.google.parentPath | string | `nil` | See https://cloud.google.com/translate/docs/migrate-to-v3#resources_projects_and_locations for details |
| config.logLevel | string | `nil` | Which python log level to use DEBUG being the most verbose. INFO is recommended |
| config.microsoft | object | `{"endpoint":null,"region":"global","usingVirtualNetwork":false}` | Configuration related to the microsoft translator engine |
| config.microsoft.endpoint | string | `nil` | The HTTP endpoint for requests to the microsoft translator service |
| config.microsoft.region | string | `"global"` | Which region the microsoft translator service is in |
| config.microsoft.usingVirtualNetwork | bool | `false` | See docs for relevance (values are true or false) https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-reference#virtual-network-support: |
| config.papago | object | `{"endpoint":"https://openapi.naver.com/v1/papago/n2mt","naverCloud":false}` | Configuration related to Naver's Papago translate |
| config.papago.endpoint | string | `"https://openapi.naver.com/v1/papago/n2mt"` | The papago HTTP endpoint |
| config.papago.naverCloud | bool | `false` | boolean indicating whether the service is from Naver Cloud (true) or Naver Developers (false) |
| config.yandex | object | `{"endpoint":"https://translate.api.cloud.yandex.net/translate/v2/","folderId":null}` | Configuration related to the Yandex Translation service |
| config.yandex.endpoint | string | `"https://translate.api.cloud.yandex.net/translate/v2/"` | The Yandex translation HTTP endpoint |
| config.yandex.folderId | string | `nil` | The Yandex Cloud folder ID if a UserAccount is used for authentication |
| fullnameOverride | string | `""` |  |
| image | string | `"docker.io/restd/multi-translate:latest"` | The application docker image |
| imagePullPolicy | string | `"IfNotPresent"` | The pull policy for the application docker image |
| imagePullSecrets | list | `[]` | Any pull secrets required to pull the application, initContainers, or sidecars |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths | list | `[]` |  |
| ingress.tls | list | `[]` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| postgresql.enabled | bool | `true` |  |
| postgresql.existingSecret | string | `""` |  |
| postgresql.existingSecretKey | string | `"postgresql-password"` |  |
| postgresql.persistence.accessModes[0] | string | `"ReadWriteOnce"` |  |
| postgresql.persistence.enabled | bool | `true` |  |
| postgresql.persistence.size | string | `"8Gi"` |  |
| postgresql.persistence.storageClass | string | `""` |  |
| postgresql.postgresqlDatabase | string | `"translate"` |  |
| postgresql.postgresqlPassword | string | `"SuperSecretChangeMe"` |  |
| postgresql.postgresqlUsername | string | `"postgres"` |  |
| replicaCount | int | `1` | The number of replicas of the application to create |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `nil` |  |
| tolerations | list | `[]` |  |
