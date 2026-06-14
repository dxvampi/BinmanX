package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	args := os.Args
	fmt.Println(args)
	if len(args) < 2 {
		fmt.Println("You need to provide a command")
		return
	}
	switch args[1] {
	case "list":
		fmt.Println("-- LIST OF CONFIGURED ALIASES FOR BINARIES --")
		fmt.Println("example (example/route/to/bin)")
		fmt.Println("example2 (example/route/to/bin2)")
		fmt.Println("--------------- END OF LIST -----------------")
	case "configure", "config":
		reader := bufio.NewReader(os.Stdin)
		fmt.Println("-- BINARY ALIASES CONFIGURATION --")
		fmt.Print("Path to the binary -> ")
		pathToAlias, _ := reader.ReadString('\n')
		pathToAlias = strings.TrimSpace(pathToAlias)
		fmt.Printf("Alias to assing to %s -> ", pathToAlias)
		aliasToPath, _ := reader.ReadString('\n')
		aliasToPath = strings.TrimSpace(aliasToPath)
		fmt.Printf("Alias: %s assigned correctly to %s!\n", aliasToPath, pathToAlias)
		fmt.Println("-------- END OF CONFIGURE --------")
	default:
		fmt.Printf("Unknown command '%s'\n", args[1])
	}
}
