package cleanparser


type CleanProcessor interface {
	Begin()
	BeginLine()
	Process(word string, num uint32, col int)
	EndLine()
	End()
}


type TfDf struct {
	Tf uint32
	Df uint32
}

type IdTfDf struct {
	Id int
	Tfdf TfDf
}

const (
	ID = 0
	TITLE = 1
	BODY = 2
)

