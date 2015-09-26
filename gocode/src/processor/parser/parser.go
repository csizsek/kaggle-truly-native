package main

import (
  "fmt"
  "os"
  "io/ioutil"
  "processor/utilities"
  "strings"
)

func main() {

  fileb, err := ioutil.ReadFile(os.Args[1])
  stopwords
  file := string(fileb)
  if err != nil {
    fmt.Println("Error:", err)
    return
  }

  file = strings.Replace(file, "&lt;", "<", -1)
  file = strings.Replace(file, "&gt;", ">", -1)

  title := make(map[string]int)
  body := make(map[string]int)
  meta := make(map[string]int)

  utilities.ParseHtml(file, title, body, meta)

  fmt.Printf("%s |", os.Args[1])
  for key, val := range title {
    fmt.Printf(" %s:%d ", key, val)
  }
  fmt.Printf(" |")
  for key, val := range body {
    fmt.Printf(" %s:%d", key, val)
  }
  fmt.Printf("\n")
}
