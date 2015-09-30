package cleanparser

import (
	"os"
	"bufio"
	"math"
	"fmt"
	"strings"
	"strconv"
)


type OkapiProcessor struct {
	dict map[string]IdTfDf
	b float64
	k1 float64
	numDocs uint32
	avgdl float64
	dictfile string

	id string
	docLength uint32
	titleWords map[string]uint32
	bodyWords map[string]uint32
	weightTitle float64
	weightBody	float64
}

func NewOkapiProcessor(b float64, k1 float64, numDocs uint32, avgdl float64, weightTitle float64, weightBody float64, dictfile string) *OkapiProcessor {
	return &OkapiProcessor{b:b, k1:k1, dictfile:dictfile, numDocs:numDocs, avgdl:avgdl, weightTitle:weightTitle, weightBody:weightBody}
}

func (op *OkapiProcessor) Begin() {
	op.dict = make(map[string]IdTfDf)

	file, err := os.Open(op.dictfile)
	if err != nil {
		fmt.Errorf(err.Error())
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		cols := strings.Split(scanner.Text(), " ")
		if (len(cols) != 4) {
			fmt.Errorf("Bad line format in dictionary")
			continue
		}

		id, _ := strconv.ParseInt(cols[0], 10, 0)
		tf, _ := strconv.ParseUint(cols[2], 10, 0)
		df, _ := strconv.ParseUint(cols[3], 10, 0)

		op.dict[cols[1]] = IdTfDf{Id:int(id), Tfdf:TfDf{Tf:uint32(tf), Df:uint32(df)}}
	}

	if err := scanner.Err(); err != nil {
		fmt.Errorf(err.Error())
	}
}

func (op *OkapiProcessor) BeginLine() {
	op.docLength = 0
	op.titleWords = make(map[string]uint32, 0)
	op.bodyWords = make(map[string]uint32, 0)
}

func (op *OkapiProcessor) Process(word string, num uint32, col int) {
	switch (col) {
	case ID:
		op.id = word
	case TITLE:
		op.docLength += num
		op.titleWords[word] = num
	case BODY:
		op.docLength += num
		op.bodyWords[word] = num

	}
}

func (op *OkapiProcessor) EndLine() {
	scores := make(map[int]float64)

	for word, num := range op.titleWords {
		if idtfdf, ok := op.dict[word]; ok {
			scores[idtfdf.Id] += op.weightTitle*op.idf(word, idtfdf)*op.tf(word, num)
		}
	}

	for word, num := range op.bodyWords {
		if idtfdf, ok := op.dict[word]; ok {
			scores[idtfdf.Id] += op.weightBody*op.idf(word, idtfdf)*op.tf(word, num)
		}
	}

	fmt.Printf("%s", op.id)
	for id, score := range scores {
		if score > 0.0 {
			fmt.Printf(" %d:%f", id, score)
		}
	}
	fmt.Printf("\n")
}

func (op* OkapiProcessor) End() {

}

func (op *OkapiProcessor) idf (word string, idtfdf IdTfDf) float64 {
	return math.Max(math.Log2((float64(op.numDocs) - float64(idtfdf.Tfdf.Df) + 0.5)/(float64(idtfdf.Tfdf.Df) + 0.5)), 0.0)
}

func (op *OkapiProcessor) tf (word string, num uint32) float64 {
	return float64(num)*(op.k1 + 1)/(float64(num) + op.k1*(1 - op.b + op.b*float64(op.docLength)/op.avgdl))
}
