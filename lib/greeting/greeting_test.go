package greeting

import (
	"testing"

	. "github.com/jfmatt/gotest"
)

func TestGetGreeting(t *testing.T) {
	ExpectThat(t, GetGreeting("Alice"), StartsWith("Greetings"))
	ExpectThat(t, GetGreeting("Alice"), HasSubstr("Alice"))
}
