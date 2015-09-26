package utilities

import (
	"strings"
	_ "github.com/reiver/go-porterstemmer"
	"github.com/kljensen/snowball"
	"golang.org/x/net/html"
	"text/scanner"
	_ "fmt"
	"fmt"
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
				words[stem] += 1
			}
		}
		tok = s.Scan()
	}
}