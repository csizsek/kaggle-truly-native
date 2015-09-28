package main

import (
	"os"
	"processor/utilities"
	"processor/cleanparser"
)


func main() {

	utilities.ParseCleanFiles(os.Args[1:], &cleanparser.DictProcessor{})

}