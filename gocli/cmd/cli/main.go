package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/jfmatt/snapfold/lib/greeting"
)

var rootCmd = &cobra.Command{
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
	},
}

func init() {
	// Add the greet command from the shared library
	rootCmd.AddCommand(greeting.NewGreetCommand())
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
