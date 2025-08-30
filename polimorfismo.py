class Animal:
    def fazer_som(self):
        pass

class Cachorro(Animal):
    def fazer_som(self):
        return "Au Au"
    
class Gato(Animal):
    def fazer_som(self):
        return "meau"
    
#usando o polimorfismo

def fazer_animal_falar(animal: Animal):
    print(animal.fazer_som())

jade = Cachorro()
romeu = Gato()

fazer_animal_falar(jade)
