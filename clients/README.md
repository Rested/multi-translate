## Examples

### Python

Install
```bash
pip install git+https://github.com/rekon-oss/multi-translate.git#egg=multitranslateclient\&subdirectory=clients/python
```

Usage
```
import multitranslateclient

def translate():
    config = multitranslateclient.configuration.Configuration(host="http://localhost:8080")
    client = multitranslateclient.api_client.ApiClient(configuration=config)
    mt_client = multitranslateclient.api.DefaultApi(api_client=client)
    translation: multitranslateclient.models.TranslationResponse = mt_client.translate_translate_get(
        source_text="hola",
        to_language="en"
    )
    print(f"translation: {translation.translated_text}")


if __name__ == '__main__':
    translate()
```

### Go

Install
```bash
go get -u github.com/rekon-oss/multi-translate/clients/go
```

Usage
```go
package main

import (
	"fmt"
	"log"
	"github.com/rekon-oss/multi-translate/clients/go"
)
import "context"

func main() {
	cfg := multitranslateclient.NewConfiguration()
	cfg.Host = "localhost:8080"
	client := multitranslateclient.NewAPIClient(cfg)
	resp, _, err := client.DefaultApi.TranslateTranslateGet(context.TODO(), "hello", "es", &multitranslateclient.TranslateTranslateGetOpts{})
	if err != nil {
		log.Fatal("something went wrong!")
	}
	fmt.Printf("translation is %s", resp.TranslatedText)
}
```



## Generation

#### Python
```bash
version=$(<VERSION)
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g python -o /local/clients/python --package-name multitranslateclient \
--git-user-id rekon-oss --git-repo-id multi-translate \
--additional-properties=packageVersion=$version
```

#### Go

```bash
version=$(<VERSION)
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g go -o /local/clients/go --package-name multitranslateclient \
--git-user-id rekon-oss --git-repo-id multi-translate/clients/go \
--additional-properties=packageVersion=$version,packageUrl=https://github.com/rekon-oss/multi-translate/clients/python
```

#### Javascript 
```bash
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g javascript -o /local/clients/js --package-name multitranslateclient \
--git-user-id rekon-oss --git-repo-id multi-translate \
--additional-properties=npmRepository=https://npm.pkg.github.com/rekon-oss,projectName=multi-translate
```