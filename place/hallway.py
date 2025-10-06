from .wall import Wall


class Hallway:
    def __init__(self, x=0.0, z=0.0, width=5.0, length=5.0, height=3.0):
        """
        Inicializa um corredor com paredes laterais e teto.

        Args:
            x: Posição X (centro)
            z: Posição Z (centro do corredor)
            width: Largura do corredor (direção X)
            length: Comprimento do corredor (direção Z)
            height: Altura do corredor
        """
        self.x = x
        self.z = z
        self.width = width
        self.length = length
        self.height = height

        # Cria paredes laterais (ao longo da direção Z)
        wall_thickness = 0.2
        left_x = x - width / 2 - wall_thickness / 2
        right_x = x + width / 2 + wall_thickness / 2

        # Parede esquerda (se estende ao longo de Z)
        self.wall_left = Wall(x=left_x, z=z, width=wall_thickness, height=height, depth=length)
        # Parede direita (se estende ao longo de Z)
        self.wall_right = Wall(x=right_x, z=z, width=wall_thickness, height=height, depth=length)

        # Teto abrange a largura e o comprimento
        from .ceiling import Ceiling
        self.ceiling = Ceiling(x=x, y=height, z=z, width=width, depth=length)

    def add_to_framework(self, framework):
        """
        Adiciona todos os componentes do corredor a um framework de cenário.

        Args:
            framework: Instância de PlaceFramework para adicionar elementos
        """
        framework.add_element(self.wall_left)
        framework.add_element(self.wall_right)
        framework.add_element(self.ceiling)

    def get_elements(self):
        """
        Obtém todos os elementos do corredor como uma lista.

        Returns:
            list: Lista de objetos PlaceElement (paredes e teto)
        """
        return [self.wall_left, self.wall_right, self.ceiling]
