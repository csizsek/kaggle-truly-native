package cleanparser

import (
	"fmt"
)

type AvgLengthProcessor struct {
	count uint64
	sumlength uint64
}

func (ap *AvgLengthProcessor) Begin() {
	ap.count = 0
}

func (ap *AvgLengthProcessor) BeginLine() {
	ap.count++
}

func (ap *AvgLengthProcessor) Process(word string, num uint32, col int) {
	switch (col) {
	case TITLE:
		break
	default:
		ap.sumlength += uint64(num)
	}
}

func (ap *AvgLengthProcessor) EndLine() {

}

func(ap *AvgLengthProcessor) End() {
	fmt.Printf("Count: %d AvgLength: %f", ap.count, float64(ap.sumlength)/float64(ap.count))
}