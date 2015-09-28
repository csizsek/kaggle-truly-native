package main

import (
  "fmt"
  "os"
  "io/ioutil"
  "bufio"
  "processor/utilities"
  "strings"
  "path/filepath"
  "strconv"
)


func main() {
  stopwords := make(map[string]int)
  skipDocs := 0
  if len(os.Args) > 3 {
    skipDocs, _ = strconv.Atoi(os.Args[3])
  }

  fileSW, err := os.Open(os.Args[2])
  if err != nil {
    fmt.Errorf("Couldn't open stopwords file: %s", err.Error())
  }
  defer fileSW.Close()

  scanner := bufio.NewScanner(fileSW)
  for scanner.Scan() {
    stopwords[string(scanner.Text())]=1
  }

  if err := scanner.Err(); err != nil {
    fmt.Errorf("Error reading stopwords file: %s", err.Error())
  }

  numFile := 0
  filepath.Walk(os.Args[1], func(path string, f os.FileInfo, err error) error {
    if f.IsDir() {
      return nil
    }

    if numFile < skipDocs {
      numFile++
      return nil
    }
    fileb, err := ioutil.ReadFile(path)
    file := string(fileb)
    if err != nil {
      fmt.Println("Error:", err)
      return err
    }

    file = strings.Replace(file, "&lt;", "<", -1)
    file = strings.Replace(file, "&gt;", ">", -1)

    title := make(map[string]int)
    body := make(map[string]int)
    meta := make(map[string]int)

    utilities.ParseHtml(file, stopwords, title, body, meta)
    last := strings.LastIndex(path, "/")
    var fname string
    if (last > -1) {
      fname = path[last+1:]
    }
    fmt.Printf("%s |", fname)
    for key, val := range title {
      fmt.Printf(" %s:%d ", key, val)
    }
    fmt.Printf(" |")
    for key, val := range body {
      fmt.Printf(" %s:%d", key, val)
    }
    fmt.Printf("\n")
    return nil
  })
}
