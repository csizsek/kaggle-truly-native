package main

import (
	"os"
	"processor/utilities"
	"processor/cleanparser"
	"flag"
)


func main() {
	var b = flag.Float64("b", 0.75, "Okapi b paramter")
	var k1 = flag.Float64("k1", 1.5, "Okapi k1 paramter")
	var numDocs = flag.Uint64("numdocs", 404076, "Num documents in the corpus")
	var avgdl = flag.Float64("avgdl", 632.651885, "Avarage doument length")
	var wtitle = flag.Float64("wtitle", 5.0, "Title weight")
	var wbody = flag.Float64("wbody", 1.0, "Title body")
	var dictfile = flag.String("dictfile", "tmp/dict_sorted.txt", "Dictionary file")

	flag.Parse()

	nflag := flag.NFlag()


	okapiProcessor := cleanparser.NewOkapiProcessor(*b, *k1, uint32(*numDocs), *avgdl, *wtitle, *wbody, *dictfile)

	utilities.ParseCleanFiles(os.Args[nflag+1:], okapiProcessor)

}