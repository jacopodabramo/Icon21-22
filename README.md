# Icon21-22
Repository per il progetto di Ingegneria della Conoscenza 

# Esecuzione 
Creare l'ambiente virtuale

<code> cd Icon21-22 </code>

<code> python -m venv icon21-22 </code>

**Importante eseguire i run nell'ordine in cui sono posti almeno per la prima volta**<br>

 Fase di preprocessing <br>

<code> python preprocessing/cleaning.py ./datasets/listings.csv </code>
 
 Clustering <br>

<code> python clustering/clustering.py ./datasets/cleaned_dataset.csv [number of clusters] [number of iterations] </code>
 
 Knowledge Base <br>

<code> python KnowledgeBase/Kb.py ./datasets/prolog_dataframe.csv </code>
 
 User Interface <br>

<code> python UI/ui.py </code>


