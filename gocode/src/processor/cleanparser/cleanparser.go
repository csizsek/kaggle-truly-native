package cleanparser

import (
	"os"
	"fmt"
	"bufio"
	"strings"
)

type TfDf struct {
	Tf uint32
	Df uint32
}


func main() {
	dict := make(map[string]TfDf)

	fileSW, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Errorf("Couldn't open stopwords file: %s", err.Error())
	}
	defer fileSW.Close()

	scanner := bufio.NewScanner(fileSW)
	for scanner.Scan() {
		line := scanner.Text()

		cols := strings.Split(line, "|")

		for i := 1; i <= 2; i++ {
			words := strings.Split(cols[i], " ")
			for _, val := range words {
				var num uint32
				var word string
				fmt.Sscanf(val, "%s:%u", word, num)

				if tfdf, ok := dict[word]; ok {
					tfdf.Tf += num;
					tfdf.Df++
					dict[word] = tfdf
				} else {
					dict[word] = TfDf{Tf:num, Df:1}
				}
			}
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Errorf("Error reading stopwords file: %s", err.Error())
	}

	for word, tfdf := range dict {
		fmt.Printf("%s %u %u", word, tfdf.Tf, tfdf.Df)
	}
}