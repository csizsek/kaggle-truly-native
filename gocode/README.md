## Install:
1. Install the freshest version of [go](https://golang.org/doc/install)
2. Clone this repository
3. 
```console
$ cd kaggle-truly-nateive/gocode/
$ export GOPATH=`pwd`
$ export PATH=$PATH:$GOPATH/bin
```

## Build:
```console
$ go get github.com/tools/godep
$ godep restore
```

## Create your clean text processor
1. Create a struct which implements the CleanProcessor interface: src/processor/cleanparser/cleanparser.go just like: 
[statsprocessor](https://github.com/csizsek/kaggle-truly-native/blob/master/gocode/src/processor/cleanparser/statsprocessor.go), [okapiprocessor](https://github.com/csizsek/kaggle-truly-native/blob/master/gocode/src/processor/cleanparser/okapiprocessor.go)
2. Create the main runnable just like: [dictsparser](https://github.com/csizsek/kaggle-truly-native/blob/master/gocode/src/processor/main/dictparser/dictparser.go), [okapiparser](https://github.com/csizsek/kaggle-truly-native/blob/master/gocode/src/processor/main/okapiparser/okapiparser.go)
3. 
```console
$ go install processor/main/yourparser
```

## Run
```console
$ yourparser <args>
```
