package main

import (
	"runtime/debug"
	"net/http"
	"weblog/internal/common"

	graphqltrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/graph-gophers/graphql-go"
	httptrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/net/http"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"

	graphql "github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/relay"
)

const schema = `
directive @case(format: String) on FIELD

type Query {
	user(id: Int!): User
	userByName(name: String): [User!]!
}

type User {
	id: Int!
	name: String!
}
`

func main() {
	tracer.Start()
	defer tracer.Stop()

	schema := graphql.MustParseSchema(schema, &query{}, graphql.Tracer(graphqltrace.NewTracer()))
	handler := &relay.Handler{Schema: schema}

	mux := httptrace.NewServeMux()
	mux.Handle("/graphql", handler)

	// The / endpoint is used as a weblog heartbeat
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// "/" is the default route when the others don't match
		// cf. documentation at https://pkg.go.dev/net/http#ServeMux
		// Therefore, we need to check the URL path to only handle the `/` case
		if r.URL.Path != "/" {
			w.WriteHeader(http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusOK)
	})

	mux.HandleFunc("/healthcheck", func(w http.ResponseWriter, r *http.Request) {
		var tracerVersion string
		var libddwafVersion string

		if bi, ok := debug.ReadBuildInfo(); ok {
			for _, mod := range bi.Deps {
				println(mod.Path, mod.Version)

				if mod.Path == "gopkg.in/DataDog/dd-trace-go.v1" {
					tracerVersion = mod.Version
				} else if mod.Path == "github.com/DataDog/go-libddwaf/v3" {
					libddwafVersion := mod.Version
				}
			}
		}

        if tracerVersion == "" {
            http.Error(w, "Can't get dd-trace-go version", http.StatusInternalServerError)
            return
        }

		appsec_rules_version, err := os.ReadFile("SYSTEM_TESTS_APPSEC_EVENT_RULES_VERSION")
        if err != nil {
            http.Error(w, "Can't get SYSTEM_TESTS_APPSEC_EVENT_RULES_VERSION", http.StatusInternalServerError)
            return
        }
		
        libray := map[string]interface{}{
            "language":  "golang",
            "version":   string(tracerVersion),
            "appsec_event_rules_version": string(appsec_rules_version),
			"libddwaf_version": libddwafVersion,
        }

        data := map[string]interface{}{
            "status": "ok",
            "library": libray,
        }

        jsonData, err := json.Marshal(data)
        if err != nil {
            http.Error(w, "Can't build JSON data", http.StatusInternalServerError)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        w.Write(jsonData)
	})

	common.InitDatadog()

	panic(http.ListenAndServe(":7777", mux))
}

type query struct{}

func (query) User(args struct{ ID int32 }) *user {
	if name, found := users[args.ID]; found {
		return &user{id: args.ID, name: name}
	}
	return nil
}

func (query) UserByName(args struct{ Name *string }) []*user {
	if args.Name == nil {
		args.Name = new(string)
	}

	result := make([]*user, 0, len(users))
	for id, name := range users {
		if name == *args.Name {
			result = append(result, &user{id: id, name: name})
		}
	}
	return result
}

type user struct {
	id   int32
	name string
}

func (u *user) ID() int32 {
	return u.id
}

func (u *user) Name() string {
	return u.name
}

var users = map[int32]string{
	1: "foo",
	2: "bar",
	3: "bar",
}
