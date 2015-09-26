package dists

import (
	"math"
)

func Js (words_left map[string]int, words_right map[string]int) float64 {
	len_left, len_right := 0, 0

	for _, val := range words_left {
		len_left += val
	}

	for _, val := range words_right {
		len_right += val
	}

	dist := 0.0
	for key, val := range words_left {
		p := float64(val)/float64(len_left)
		q := 0.0
		if (len_right > 0) {
			q = float64(words_right[key])/float64(len_right)
		}
		dist += p*math.Log2(2*p/(p + q))
	}

	for key, val := range words_right {
		p := float64(val)/float64(len_right)
		q := 0.0
		if (len_left > 0) {
			q = float64(words_left[key])/float64(len_left)
		}
		dist += p*math.Log2(2*p/(p + q))
	}

	return dist
}

