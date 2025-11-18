module github.com/jfmatt/snapfold/gocli

go 1.24

require (
	github.com/jfmatt/snapfold/lib v0.0.0
	github.com/spf13/cobra v1.8.1
)

require (
	github.com/inconshreveable/mousetrap v1.1.0 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
)

replace github.com/jfmatt/snapfold/lib => ../lib
