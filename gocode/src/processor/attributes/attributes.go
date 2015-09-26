package main

import(
	"common"
	"os"
	"io/ioutil"
	"encoding/json"
	"fmt"
	"dists"
)

func main() {
	js, _ := ioutil.ReadFile(os.Args[1])
	docs := make([]common.Document, 0)
	err := json.Unmarshal(js, &docs)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
	}

	for _, val := range docs {
		fmt.Printf("%d %f %d\n", val.Id, dists.Js(val.Query, val.Description), val.Relevance)
	}
}