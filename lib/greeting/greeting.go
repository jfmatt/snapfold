package greeting

import (
	"fmt"

	"github.com/spf13/cobra"
)

// NewGreetCommand creates a new cobra command for greeting
func NewGreetCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "greet [name]",
		Short: "Greet someone (from shared lib)",
		Args:  cobra.MaximumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			name := "World"
			if len(args) > 0 {
				name = args[0]
			}
			fmt.Printf("Hello, %s! (from shared library)\n", name)
		},
	}
}

// GetGreeting returns a greeting message
func GetGreeting(name string) string {
	if name == "" {
		name = "World"
	}
	return fmt.Sprintf("Greetings from the shared library, %s!", name)
}
