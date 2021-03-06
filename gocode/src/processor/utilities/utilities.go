package utilities

import (
	"strings"
	_ "github.com/reiver/go-porterstemmer"
	"github.com/kljensen/snowball"
	"golang.org/x/net/html"
	"text/scanner"
	"fmt"
	"os"
	"bufio"
	"strconv"
	"processor/cleanparser"
)

func ParseHtml(rec string, stopwords map[string]int, title map[string]int, body map[string]int, meta map[string]int) {
	r := strings.NewReader(rec)
	html_parser := html.NewTokenizer(r)

	ignoretags := make(map[string]int)
	ignoretags["script"] = 1
	ignoretags["style"] = 1

	in_title := false

	stack := Stack{}

	//fmt.Println("Record", lineCount, "is", record, "and has", len(record), "fields")

	cont := true
	for ; cont; {
		token := html_parser.Next()
		switch token {
		case html.ErrorToken:
			// Returning io.EOF indicates success.
			cont = false
			break
		case html.TextToken:
			if stack.Len() == 0 {
				if in_title {
					Tokenize(string(html_parser.Text()), stopwords, title)
				} else {
					Tokenize(string(html_parser.Text()), stopwords, body)
				}
			}
		case html.StartTagToken:
			tagbyte, _ := html_parser.TagName()
			tag := string(tagbyte)
			if tag == "title" {
				in_title = true
			}

			//fmt.Printf("Tag: %s\n", tag)
			if _, ok := ignoretags[tag]; ok {
				//fmt.Printf("Found ignore tag: %s\n", tag)
				stack.Push(html_parser.Text())
			}
		case html.EndTagToken:
			tagbyte, _ := html_parser.TagName()
			tag := string(tagbyte)
			if tag == "title" {
				in_title = false
			}

			//fmt.Printf("Close tag: %s\n", tag)
			if _, ok := ignoretags[tag]; ok {
				//fmt.Printf("Found ignore close tag: %s\n", tag)
				stack.Pop()
			}
		}
	}
}

func Tokenize(text string, stopwords map[string]int, words map[string]int) {
	var s scanner.Scanner
	s.Init(strings.NewReader(text))
	tok := s.Scan()
	for tok != scanner.EOF {
		if tok == scanner.String {
			Tokenize(strings.Trim(s.TokenText(), "\"`"), stopwords, words)
		} else if tok == scanner.Char {
			Tokenize(strings.Trim(s.TokenText(), "'"), stopwords, words)
		} else if tok == scanner.Ident {
			word := s.TokenText()
			if _, ok := stopwords[word]; !ok && len(word) > 2 {
				stem, err := snowball.Stem(word, "english", true)
				if err != nil {
					fmt.Errorf("Couldnt stem word: %s", word)
					stem = word
				}
				if _, ok := stopwords[stem]; !ok {
					words[stem] += 1
				}
			}
		}
		tok = s.Scan()
	}
}

func ParseCleanFiles(files []string, processor cleanparser.CleanProcessor) {

	processor.Begin()
	for _, file := range files {
		fileSW, err := os.Open(file)
		if err != nil {
			fmt.Errorf("Couldn't open file: %s", err.Error())
			return
		}
		defer fileSW.Close()
		reader := bufio.NewReaderSize(fileSW, 4*1024)


		liner, isPrefix, err := reader.ReadLine()
		for err == nil {
			var line string
			if isPrefix {
				for isPrefix {
					line = line + string(liner)
					liner, isPrefix, err = reader.ReadLine()
				}
			} else {
				line = string(liner)
			}

			processor.BeginLine()
			cols := strings.Split(line, "|")

			if len(cols) != 3 {
				fmt.Errorf("Wrong line format: %s", line)
				liner, isPrefix, err = reader.ReadLine()
				continue
			}
			processor.Process(cols[0], 0, 0)
			for i := 1; i <= 2; i++ {
				words := strings.Split(cols[i], " ")
				for _, val := range words {
					var num uint32
					var word string

					vect := strings.Split(val, ":")
					if len(vect) != 2 {
						continue
					}
					word = vect[0]
					tmp, _ := strconv.Atoi(vect[1])
					num = uint32(tmp)
					processor.Process(word, num, i)
				}
			}
			processor.EndLine()
			liner, isPrefix, err = reader.ReadLine()
		}
	}
	processor.End()
}
