package main

import (
	"os"
	"processor/utilities"
	"processor/cleanparser"
)


func main() {

	utilities.ParseCleanFile(os.Args[1], &cleanparser.DictProcessor{})

}