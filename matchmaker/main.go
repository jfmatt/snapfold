package main

import (
	"fmt"
	"os"

	"github.com/jfmatt/flagr"
	"github.com/spf13/cobra"
)

func main() {
	c := &cobra.Command{
		Use:   "matchmaker",
		Short: "snapfold matchmaker server and utilities",
	}

	c.AddCommand(MigrationCommand())
	c.AddCommand(ServerCommand())

	if err := c.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

type MigrateArgs struct {
	Dsn string
}

func MigrationCommand() *cobra.Command {
	c := &cobra.Command{
		Use:   "migrate",
		Short: "Update database schemas",
	}
	c.RunE = flagr.Run(c, Migrate)
	return c
}

func Migrate(flags *MigrateArgs, cmd *cobra.Command, args []string) error {
	return nil
}

func ServerCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "serve",
		Short: "Serve login and matchmaking server",
	}
}

func ServeHttp(cmd *cobra.Command, args []string) error {
	return nil
}
