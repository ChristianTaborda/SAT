
#Rango de instancias SAT a recorrer en la carpeta:
rango=$(ls InstanciasSAT/*)

for instancia in $rango
do
	#Obtención del nombre del archivo con la instancia SAT:
	reduccion=$(echo $instancia | cut -c 15-)

	#Creación del archivo para la instancia X-SAT:
	touch X-SAT/$reduccion

	#Transcripción del formato DIMACS al nuevo archivo:
	python3 Reductor/Reductor.py $instancia $2 > X-SAT/$reduccion

	echo "Instancia" $reduccion "reducida con éxito."
done
