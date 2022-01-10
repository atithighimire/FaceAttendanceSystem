package main

import(
	"fmt"
	"image"
	"os"
)
func main() {
	var paths []string
	paths = append(paths, "E:\Attendace_management_system\StudentDetails\StudentDetails.csv")
	var labels []string
	labels = append(labels,"TrainingImage")
	
	var images []image.Image

	for index := 0; index < len(paths); index++ {
		img, err := loadImage(paths[index])
		checkError(err)
		images = append(images, img)
	}
	params := lbph.Params{
		Radius:    1,
		Neighbors: 8,
		GridX:     8,
		GridY:     8,
	}

	lbph.Init(params)
	err := lbph.Train(images, labels)
	checkError(err)


	paths = nil
	paths = append(paths, "E:\Attendace_management_system\StudentDetails\StudentDetails.csv")
	
	var expectedLabels []string
	expectedLabels = append(expectedLabels, "TrainingImage")
	lbph.Metric = metric.EuclideanDistance
	for index := 0; index < len(paths); index++ 
		img, err := loadImage(paths[index])
		checkError(err)
		label, distance, err := lbph.Predict(img)
		checkError(err)
		if label == expectedLabels[index] {
			fmt.Println("Image correctly predicted")
		} else {
			fmt.Println("Image wrongly predicted")
		}
		fmt.Printf("Predicted as %s expected %s\n", label, expectedLabels[index])
		fmt.Printf("Distance: %f\n\n", distance)
	}
}
func loadImage(filePath string) (image.Image, error) {
	fImage, err := os.Open(filePath)
	checkError(err)

	defer fImage.Close()

	img, _, err := image.Decode(fImage)
	checkError(err)

	return img, nil
}
func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
}
