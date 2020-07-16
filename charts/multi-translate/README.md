multi-translate
===============
A unified interface on top of various translate APIs providing optimal translations, persistence, fallback.

Current chart version is `0.8.0`



## Chart Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | redis | 10.7.9 |
| https://kubernetes-charts.storage.googleapis.com/ | postgresql | 8.6.4 |

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| config | object | see below | Multi-Translate configuration |
| config.amazon | object | see below | Configuration related to amazon translate |
| config.amazon.awsAccessKeyIdSecret.key | string | `nil` | The key of the k8s secret containing the aws access key id |
| config.amazon.awsAccessKeyIdSecret.name | string | `nil` | The name of the k8s secret containing the aws access key id |
| config.amazon.awsSecretAccessKeySecret.key | string | `nil` | The name of the k8s secret containing the aws secret access key |
| config.amazon.awsSecretAccessKeySecret.name | string | `nil` | The name of the k8s secret containing the aws secret access key |
| config.amazon.region | string | `nil` | The aws region your amazon translate service belongs to |
| config.cors.enabled | bool | `false` | whether to enable cors |
| config.cors.originRegex | string | `nil` | a regex to match origins to allow |
| config.deepL | object | see below | Configuration related to the Deep L Translation service |
| config.deepL.authKeySecret.key | string | `nil` | The key of the k8s secret containing the deepL auth key |
| config.deepL.authKeySecret.name | string | `nil` | The name of the k8s secret containing the deepL auth key |
| config.deepL.endpoint | string | `"https://api.deepl.com/v2/"` | The deepL HTTP endpoint |
| config.google | object | see below | Configuration related to google translate |
| config.google.parentPath | string | `nil` | See https://cloud.google.com/translate/docs/migrate-to-v3#resources_projects_and_locations for details |
| config.google.serviceAccountSecret.key | string | `nil` | The key of the k8s secret containing the service account json |
| config.google.serviceAccountSecret.name | string | `nil` | The name of the k8s secret containing the service account json |
| config.gqlEnabled | bool | `true` | determines whether the /gql endpoint is available or not |
| config.languagePreferences | object | `{}` | replaces the language preferences yaml file if set |
| config.logLevel | string | `nil` | Which python log level to use DEBUG being the most verbose. INFO is recommended |
| config.maxSourceTextLength | string | `nil` | maximum size in characters of a piece of text to be translated |
| config.microsoft | object | see below | Configuration related to the microsoft translator engine |
| config.microsoft.endpoint | string | `nil` | The HTTP endpoint for requests to the microsoft translator service |
| config.microsoft.region | string | `"global"` | Which region the microsoft translator service is in |
| config.microsoft.subscriptionKeySecret.key | string | `nil` | The secret key containing your microsoft subscription key |
| config.microsoft.subscriptionKeySecret.name | string | `nil` | The name of the k8s secret containing the microsoft subscription key |
| config.microsoft.usingVirtualNetwork | bool | `false` | See docs for relevance (values are true or false) https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-reference#virtual-network-support: |
| config.papago | object | see below | Configuration related to Naver's Papago translate |
| config.papago.clientIdSecret.key | string | `nil` |  The key of the k8s secret containing the papago client id |
| config.papago.clientIdSecret.name | string | `nil` |  The name of the k8s secret containing the papago client id |
| config.papago.clientSecretSecret.key | string | `nil` |  The key of the k8s secret containing the papago client secret |
| config.papago.clientSecretSecret.name | string | `nil` |  The name of the k8s secret containing the papago client secret |
| config.papago.endpoint | string | `"https://openapi.naver.com/v1/papago/n2mt"` | The papago HTTP endpoint |
| config.papago.naverCloud | bool | `false` | boolean indicating whether the service is from Naver Cloud (true) or Naver Developers (false) |
| config.rateLimits | string | `nil` | optional rate limiting - values as specified here https://limits.readthedocs.io/en/stable/string-notation.html e.g. "10/minute;25/hour" |
| config.yandex | object | see below | Configuration related to the Yandex Translation service |
| config.yandex.endpoint | string | `"https://translate.api.cloud.yandex.net/translate/v2/"` | The Yandex translation HTTP endpoint |
| config.yandex.folderId | string | `nil` | The Yandex Cloud folder ID if a UserAccount is used for authentication |
| fullnameOverride | string | `""` |  |
| image | string | `"rekonuk/multi-translate:v0.7.0"` | The application docker image |
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
| postgresql.enabled | bool | `true` | Note that disabling postgres will mean no persistence |
| postgresql.existingSecret | string | `""` |  |
| postgresql.existingSecretKey | string | `"postgresql-password"` |  |
| postgresql.persistence.accessModes[0] | string | `"ReadWriteOnce"` |  |
| postgresql.persistence.enabled | bool | `true` |  |
| postgresql.persistence.size | string | `"8Gi"` |  |
| postgresql.persistence.storageClass | string | `""` |  |
| postgresql.postgresqlDatabase | string | `"translate"` |  |
| postgresql.postgresqlPassword | string | `"SuperSecretChangeMe"` |  |
| postgresql.postgresqlUsername | string | `"postgres"` |  |
| redis.cluster.enabled | bool | `false` |  |
| redis.cluster.slaveCount | int | `1` |  |
| redis.enabled | bool | `false` |  |
| redis.existingSecret | string | `""` |  |
| redis.existingSecretKey | string | `"redis-password"` |  |
| redis.master.persistence.accessModes[0] | string | `"ReadWriteOnce"` |  |
| redis.master.persistence.enabled | bool | `false` |  |
| redis.master.persistence.size | string | `"2Gi"` |  |
| redis.master.persistence.storageClass | string | `""` |  |
| redis.master.resources | object | `{}` |  |
| redis.password | string | `"multitranslate"` |  |
| redis.slave.persistence.accessModes[0] | string | `"ReadWriteOnce"` |  |
| redis.slave.persistence.enabled | bool | `false` |  |
| redis.slave.persistence.size | string | `"2Gi"` |  |
| redis.slave.persistence.storageClass | string | `""` |  |
| redis.slave.resources | object | `{}` |  |
| replicaCount | int | `1` | The number of replicas of the application to create |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `nil` |  |
| tolerations | list | `[]` |  |
