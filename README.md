# Desafio Técnico - Cinnecta
A seguir, está documentado todo o pipeline para a resolução do desafio técnico proposto para a vaga de Data Engineer, da Cinnecta, realizado pelo candidato João Victor Magalhães Souza.


## Exploratory Data Analisys (EDA) e Data Treatment
A primeira coisa que fiz foi analisar primeiro, sem muitos detalhes, a estrutura geral dos dados fornecidos. Como vi que haviam mais features categóricas que contínuas, eu decidi ver então a quantidade de informações ausentes nos dados:
<br>
![Screenshot](figures/fig_overview_data.png)
<br>
De cara, como podemos observar, há alguns valores ausentes nas colunas "Description" e "CustomerID", ou seja, existem vendas cujo não se sabe quem é o comprador e vendar que não se sabe o que foi comprado, ambos casos sendo um problema.
Notei então que todos os produtos que não possuem Descrição também não possuem o ID do Cliente comprador e seu preço unitário é 0, ou seja, é informação irrelevante, que não apresenta uma semântica que possa ser útil na nossa análise e, sendo assim, decidi remover esses registros.

Outra questão que pude observar é que algumas vendas possuem produtos com preço negativo (<0). Como não tenho uma noção mais específica do negócio e nem sobre os dados, eu decidi remover esses registros visto que, comumente, tal ocorrência não faz sentido.

Notei também que algumas transações possuem produtos com Quantidade negativa. Neste caso, ao invés de removê-los, decidi considerar como uma devolução.

Por fim, para facilitar algumas análises, mudei os valores ausentes dos Clientes (em CustomerID) para "Unknown". Após esses processos, já podemos começar a obter insights úteis dos dados.

## Questão 1
### <strong>a)</strong>
Interpretei como melhor cliente aquele que traz mais dinheiro para a loja, ou seja, se tenho uma compra de X unidades e cada unidade custa Y, então preciso analisar o resultado de X*Y. Dessa forma, precisei criar uma nova variável para cada transação que me diz o total pago em cada transação. Depois, bastou agrupar os clientes e somar o quanto cada cliente trouxe para a loja no período de dados disponibilizado. Nesta análise, o melhor cliente encontrado foi "Unknown", visto que, os resultados mostram que as compras sem um cliente associado somaram o maior capital resultante. Entretanto, no gráfico abaixo são mostrados os 10 melhores clientes da loja que possuem um ID:
<br>
![Screenshot](figures/1a.png)
<br>
Podemos observar o total comprado por cada um desses clientes (não é sabido se é em dólar, euro, real ou qualquer moeda). O gráfico acima mostra então que, o cliente "14646"(em azul) é o cliente que mais trouxe capital para a loja e o cliente "15311"(em amarelo) é o 10º cliente que mais trouxe capital.

### <strong>b)</strong>
Como os melhores produtos, penso que são aqueles que foram mais vendidos no período analisado. Para descobrir isso então, já que em cada transação temos o número de unidades vendidas de determinado produto, basta agrupar os produtos e somar o valor de unidades vendidas em todas as transações de cada produto. 
<br>
![Screenshot](figures/1b.png)
<br>
A figura acima mostra que o produto mais vendido da loja no período analisado é "Wolrd War 2 Gliders Asstd Designs" com 53847 unidades vendidas.

### <strong>c)</strong>
Para ter noção do comportamento diário, temos uma variável que mostra a hora e data de cada transação. Como é diário, a hora não é relevante e, devido a esse motivo, o primeiro ajuste que fiz foi retirar dos dados essa informação acerca das horas, minutos e segundos em que a transação ocorreu. 
#### <strong>Volume</strong>
O volume de vendas foi entendido como o total de produtos vendidos em cada dia durante o período analisado. Para isso, então agrupamos por dia e por produto e realizamos a soma da quantidade de unidades vendidas em cada dia de cada um dos produtos vendidos naquele dia. Dessa forma, conseguimos analisar tranquilamente o comporamento volumétrico das vendas. Abaixo, é mostrado um gráfico com todos os dias:
<br>
![Screenshot](figures/1c_volumes.png)
<br>
Podemos notar que houve um dia, no período entre Jun/2011 e Jul/2011 que houveram mais devoluções que aquisições, explicando o valor negativo obtido. Além disso, fica claro uma maior aquisição e maior consistência no período de Nov/2011, possivelmente por conta da famosa Black Friday e as promoções que circundam o mês de Novembro e fim de ano.

#### <strong>Faturamento</strong>
Em termos de faturamento, o pensamento é similar ao anterior mas agora ao invés de olharmos somente a Quantidade, olhamos a Quantidade * Preço:
<br>
![Screenshot](figures/1c_invoice.png)
<br>
É notório que o período após Set/2011 apresenta uma consistência de faturamento em maior nível que os períodos anteriores, que pode ser possivelmente explicado pelas promoções de fim de ano, como dito anteriormente.