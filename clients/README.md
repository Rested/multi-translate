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


### Javascript

Install 

```bash
npm i @rekon-oss/multi-translate
```

```javascript
const mt = require('@rekon-oss/multi-translate')

const client = new mt.ApiClient()
client.basePath = 'http://localhost:8080'

const api = new mt.DefaultApi(client)

api.translateTranslateGet("hello world!", "fr", {}, function (e, resp) {
    if (e) {
        throw e
    }
    // bonjour le monde!
    console.log(resp.translated_text)
})
```