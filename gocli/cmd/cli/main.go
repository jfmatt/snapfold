package main

import (
	"fmt"
	"os"

	"github.com/jfmatt/snapfold/lib/greeting"
	"github.com/spf13/cobra"

	pb "github.com/jfmatt/snapfold/gamedef"
)

func rootCmd() *cobra.Command {
	c := &cobra.Command{
		Use:   "gocli",
		Short: "A simple CLI tool built with Cobra",
		Long:  `A demonstration Go binary that uses the Cobra library and a shared library module.`,
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("Hello from the Go CLI!")
			fmt.Println("Built with Cobra library")
			// Use the shared library
			fmt.Println(greeting.GetGreeting(""))
			if len(args) > 0 {
				fmt.Printf("Arguments: %v\n", args)
			}

			protoVal := &pb.TableConfig{}
			fmt.Printf("proto (%T): %s\n", protoVal, protoVal.String())
		},
	}
	c.AddCommand(greeting.NewGreetCommand())

	return c
}

func main() {
	if err := rootCmd().Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
