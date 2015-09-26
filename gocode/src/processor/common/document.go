package common

type Document struct {
	Id int						`json: id`
	Query map[string]int		`json: query`
	Title map[string]int		`json: title`
	Description map[string]int	`json: description`
	Relevance int				`json: relevance`
	Variance float64			`json: variance`
}

func NewDocument(id int, query map[string]int, title map[string]int,
				 description map[string]int, relevance int, variance float64) Document {
	d := Document{id, query, title, description, relevance, variance}
	return d
}