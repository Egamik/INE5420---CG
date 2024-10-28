# Execução
cd src

pip install -r requirements.txt

python3 main.py

# Notas
A indexação de objetos não está funcionando corretamente, teste usando apenas 1 objeto

Projeção paralela ortogonal
    - Projeção de raios perpendiculares ao plano de projeção
    - Para projetar apenas ignora eixo z e desenha arestas

# Passos projeção paralela ortogonal
1 - Transladar View Reference Point para origem (VRP)
    - Usar primeiro vértice como VRP
2 - Determinar View Plane Normal (VPN)
    - Decompor e determinar angulos de VPN com x e y
3 - Rotacionar mundo em torno do plano x y de forma a alinhar VPN com eixo z
4 - Ignorar coordenadas z do objeto
5 - Normalizar o resto (coordenadas de window)
    - Feito durante drawObjects
6 - Clip
7 - Transformar para coordenadas de viewport

Passos #1 a #3 implicam detach da viewport e sistema de coordenadas 