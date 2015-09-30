package cleanparser

import (
	"fmt"
)

type DictProcessor struct {
	lineDict map[string]uint32
	dict map[string]TfDf
}

func (dp *DictProcessor) Begin () {
	dp.dict = make(map[string]TfDf)
}

func (dp *DictProcessor) BeginLine () {
	dp.lineDict = make(map[string]uint32, 0)
}

func (dp *DictProcessor) Process (word string, num uint32, col int) {
	switch (col) {
	case ID:
		return
	default:
		dp.lineDict[word] = dp.lineDict[word] + num
	}
}

func (dp *DictProcessor) EndLine () {
	for word, num := range dp.lineDict {
		if tfdf, ok := dp.dict[word]; ok {
			tfdf.Tf += num
			tfdf.Df += 1
			dp.dict[word] = tfdf
		} else {
			dp.dict[word] = TfDf{Tf:num, Df:1}
		}
	}
}

func (dp *DictProcessor) End() {
	for word, tfdf := range dp.dict {
		fmt.Printf("%s %d %d\n", word, tfdf.Tf, tfdf.Df)
	}
}
