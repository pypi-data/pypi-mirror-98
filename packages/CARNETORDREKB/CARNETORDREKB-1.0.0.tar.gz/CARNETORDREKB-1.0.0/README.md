```python
#Nous allons faire un test pour bien vérifier que notre exchange marche bien
#Et pour également bien expliquer les règles de ce dernier
order_book = OrderBook()

# On crée des ordres limites pour donner à notre marché une profondeur

limit_orders = [{'type' : 'limit', 
                   'side' : 'ask', 
                    'quantity' : 5, 
                    'price' : 101,
                    'trade_id' : 100},
                   {'type' : 'limit', 
                    'side' : 'ask', 
                    'quantity' : 5, 
                    'price' : 103,
                    'trade_id' : 101},
                   {'type' : 'limit', 
                    'side' : 'ask', 
                    'quantity' : 5, 
                    'price' : 101,
                    'trade_id' : 102},
                   {'type' : 'limit', 
                    'side' : 'ask', 
                    'quantity' : 5, 
                    'price' : 101,
                    'trade_id' : 103},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'quantity' : 5, 
                    'price' : 99,
                    'trade_id' : 100},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'quantity' : 5, 
                    'price' : 98,
                    'trade_id' : 101},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'quantity' : 5, 
                    'price' : 99,
                    'trade_id' : 102},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'quantity' : 5, 
                    'price' : 97,
                    'trade_id' : 103},
                   ]

# On rajoute les ordres dans notre Orderbook
for order in limit_orders:
    trades, order_id = order_book.process_order(order, False, False)

# Le book courant peut être assimiler à un print
print(order_book)
# Comme nous pouvons le voir à ce moment nous avons notre order books avec les Bids, les asks et les Trades
# Il n'y a aucun trade pour le moment et c'est fait exprès quand nous avons spécifier les ordres 
# Ce sont tous des ordres limites et qui ne se croisent pas donc la résultante et qu'aucun trade ne peut s'effectuer
# Voyons également ce pourquoi nous avons choisie la structure d'arbre Bicolore car nous avons une double classification
# Pour les bids ils sont classer dans un premier temps par prix décroissant et puis par le timestamp de l'ordre au sein d'un même prix en ordre croissant
# Pour les asks ils sont classer dans un premier temps par prix en ordre croissant et puis par le timestamp des ordres au sein d'un même prix en ordre croissant
# Autrement le meilleur Ask celui qui va être privilégier pour tous ordre, qui sera prioritaire est le Ask ayant le prix le plus faible et étant arrivé le plus tôt
# Et le meilleur Bid est celui qui va être privilégier pour tous ordre Ask arrivant, le Bid qui sera prioritaire est le Bid ayant le prix le plus élevé et étant arrivé le plus tôt
# Et c'est exactement comme celà que fonctionne un exchange

print(order_book.get_best_ask())
print(order_book.get_volume_at_price('bid', order_book.get_best_bid()))
print(order_book.get_best_bid())
bids, asks, trades_done = order_book.get_all()
print(trades_done)
print(bids[0])
print(asks)
print("#########################")
# On soumet un limit order Bid qui à un prix plus élevé que le meilleur Ask soit le Ask ayant le prix le plus faible 
crossing_limit_order = {'type': 'limit',
                        'side': 'bid',
                        'quantity': 2,
                        'price': 102,
                        'trade_id': 109}

print(crossing_limit_order)
trades, order_in_book = order_book.process_order(crossing_limit_order, False, False)
print("Un Trade Prend Place car le Bid entrant croise le meilleur Ask")
print(trades)
#Or on voit qu'un trade à bien eu lieu au prix du meilleur Ask soit 101 et que 2 quantité ont été échanger
#L'élément intéressent à noter ici est bien que nous avons uniquement le premier acheteur qui a partciper à la transaction
#Et c'est bien là la preuve que nous avons bien l'ordre d'arriver des ordres qui compte c'est le meilleur Ask arrivé le plus tot qui a participer à la transaction
print(order_book)
bids, asks, trades_done = order_book.get_all()
print(trades_done[0]['prix'])
print(trades_done[0]['quantité'])
print(trades_done)
#Et là nous voyons bien comment le carnet d'ordre s'est actualisé en conséquence en effet les quantités du meilleur ordre Ask ont diminuer de 2 pour arriver à 3
print("###############")
# If a limit order bid croise le meilleur Ask mais est partiellement matché, du a un volume insuffissant à ce prix le volume restant sera
# placer dans le book comme un lim order Bid pour la quantité restant tous en respectant l'ordre toujours
big_crossing_limit_order = {'type': 'limit',
                            'side': 'bid',
                            'quantity': 50,
                            'price': 102,
                            'trade_id': 110}
print(big_crossing_limit_order)
trades, order_in_book = order_book.process_order(big_crossing_limit_order, False, False)
print("Un gros ordre bid limit croise le meilleur ask. Le volume restant est placer dans le book")
print(trades)
print(order_book)
print("###########################")

# Market Order
#Les ordres aux marché se focus plus sur la quantité quelque soit le prix 
# Les Market orders ont besoin uniquement de la spécification d'un coté (bid ou ask), une quantité, et leur trade id unique
market_order = {'type': 'market',
                'side': 'ask',
                'quantity': 40,
                'trade_id': 111}
trades, order_id = order_book.process_order(market_order, False, False)
print("#################")
print(trades)
print("#############")
print("un market order prend le volume spécifié de l'intérieur du book, quelque soit le prix")
#Les market orders consomme de la liquidité dans le marché
print("Un market ask pour 40 nous donne:")
print(order_book)
print("###############")

#A noter ici que nous considérons ici une variation du Capital à partir du moment ou l'ordre est envoyé et pas au moment 
#Ou le trade a eu lieu c'est une simplification bien sur mais en soit elle peut être justifié par le fait que par soucis 
#De simplication aucun trader ne pourras changer ou supprimer son ordre mais à noter que chaque trader peut modifier voir même
#Supprimer son ordre notre Classe OrderBook() peux gérer ce cas sans problème tous en conservant l'ordre
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def mvt_avg(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

order_book = OrderBook()
def generate_lim_orders(nb_orders, price_range_bid, price_range_ask, qte_range_ask, qte_range_bid):
  limit_orders = []
  trade_id_list = []
  for i in range(nb_orders):
    order_type = 'limit'
    alea = np.random.randint(0,2)
    if alea == 0:
      side = 'ask'
      quantity = np.random.randint(qte_range_ask[0], qte_range_ask[1]+1)
      price = np.random.randint(price_range_ask[0], price_range_ask[1]+1)
      trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
      quote = {'type' : order_type, 
               'side' : side, 
               'quantity' : quantity, 
               'price' : price,
               'trade_id' : trade_id}
      limit_orders.append(quote)
    else:
      side = 'bid'
      quantity = np.random.randint(qte_range_bid[0], qte_range_bid[1]+1)
      price = np.random.randint(price_range_bid[0], price_range_bid[1]+1)
      trade_id = 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
      quote = {'type' : order_type, 
               'side' : side, 
               'quantity' : quantity, 
               'price' : price,
               'trade_id' : trade_id}
      limit_orders.append(quote)
  return limit_orders



class Trader_quantity:

  def __init__(self, K, pnl=0, nb_actions=0):
    self.K = K
    self.K_initial = self.K
    self.nb_actions = nb_actions 
    self.pnl = pnl
    self.trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
    self.trader_balance_sheet = []
    quote = {'type' : np.nan, 
               'side' : np.nan, 
               'quantity' : np.nan, 
               'price' : np.nan,
               'trade_id' : self.trade_id}
    self.rendement_actu = self.K/self.K_initial
    dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions, 'ordre_envoyé' : quote}
    self.val=False

  def trade_first(self, order_book):
    best_ask = order_book.get_best_ask()
    best_bid = order_book.get_best_bid()
    qte_best_ask = order_book.get_volume_at_price('ask', best_ask)
    qte_best_bid = order_book.get_volume_at_price('bid', best_bid)
    vol_possible_to_buy = self.K/best_ask
    vol_possible_to_sell = self.nb_actions
    if self.K>0 and vol_possible_to_buy<qte_best_ask:
      self.order_type = 'limit'
      self.side = 'ask'
      self.quantity = vol_possible_to_buy
      self.price = best_ask
      self.last_price = best_ask
      quote = {'type' : self.order_type, 
               'side' : self.side, 
               'quantity' : self.quantity, 
               'price' : self.price,
               'trade_id' : self.trade_id}
      self.K -= vol_possible_to_buy*best_ask
      self.pnl -= vol_possible_to_buy*best_ask
      self.nb_actions += self.quantity
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions, 'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=True
    elif self.nb_actions<qte_best_bid and self.nb_actions>0:
        self.order_type = 'limit'
        self.side = 'bid'
        self.quantity = max(self.nb_actions-1,0)
        if self.quantity<=0:
          quote = {'type' : np.nan, 
                  'side' : np.nan, 
                  'quantity' : np.nan, 
                  'price' : np.nan,
                  'trade_id' : self.trade_id}
          self.rendement_actu = self.K/self.K_initial
          dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
          self.trader_balance_sheet.append(dico)
          self.val=False
        else:
          self.price = best_bid
          self.last_price = self.price
          quote = {'type' : self.order_type, 
                  'side' : self.side, 
                  'quantity' : self.quantity, 
                  'price' : self.price,
                  'trade_id' : self.trade_id}
          self.K += self.quantity*best_bid
          self.pnl += self.quantity*best_bid
          self.nb_actions -= self.quantity
          self.rendement_actu = self.K/self.K_initial
          dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
          self.trader_balance_sheet.append(dico)
          self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet
  
  def tradeSecond(self, order_book):
    if self.nb_actions>0 and self.val==True:
      best_bid = order_book.get_best_bid()
      if best_bid>self.last_price:
        self.order_type = 'limit'
        self.side = 'bid'
        self.quantity = max(self.nb_actions-1,0)
        if self.quantity<=0:
          quote = {'type' : np.nan, 
                  'side' : np.nan, 
                  'quantity' : np.nan, 
                  'price' : np.nan,
                  'trade_id' : self.trade_id}
          self.rendement_actu = self.K/self.K_initial
          dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
          self.trader_balance_sheet.append(dico)
          self.val=False
        else:
          self.price = order_book.get_best_bid()
          quote = {'type' : self.order_type, 
                  'side' : self.side, 
                  'quantity' : self.quantity, 
                  'price' : self.price,
                  'trade_id' : self.trade_id}
          self.K += self.quantity*best_bid
          self.pnl += self.quantity*best_bid
          self.nb_actions -= self.quantity
          self.rendement_actu = self.K/self.K_initial
          dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
          self.trader_balance_sheet.append(dico)
          self.val=True
      else:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet

class Trader_Buy_and_sell:

  def __init__(self, order_book):
    best_ask = order_book.get_best_ask()
    qte_best_ask = order_book.get_volume_at_price('ask', best_ask) 
    self.K = qte_best_ask*best_ask
    self.K_initial = self.K 
    self.pnl = 0
    self.trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
    self.trader_balance_sheet = []
    self.last_price = best_ask
    self.K -= self.K
    self.pnl -= self.K
    self.nb_actions = qte_best_ask
    type_order = 'limit'
    self.side = 'ask'
    quote = {  'type' : type_order, 
               'side' : self.side, 
               'quantity' : qte_best_ask, 
               'price' : best_ask,
               'trade_id' : self.trade_id}
    self.rendement_actu = self.K/self.K_initial
    dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
    self.trader_balance_sheet.append(dico)
    self.val=True

  def trade(self, order_book):
    if self.side == 'ask':
      best_bid = order_book.get_best_bid()
      qte_best_bid = max(self.nb_actions,0)
      if qte_best_bid<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        if best_bid>self.last_price:
          type_order = 'limit'
          self.side = 'bid'
          self.last_price = best_bid
          self.K += best_bid*qte_best_bid
          self.pnl += best_bid*qte_best_bid
          self.nb_actions -= qte_best_bid
          quote = {  'type' : type_order, 
                'side' : self.side, 
                'quantity' : qte_best_bid, 
                'price' : best_bid,
                'trade_id' : self.trade_id}
          self.rendement_actu = self.K/self.K_initial
          dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
          self.trader_balance_sheet.append(dico)
          self.val=True
        else:
          quote = {'type' : np.nan, 
                  'side' : np.nan, 
                  'quantity' : np.nan, 
                  'price' : np.nan,
                  'trade_id' : self.trade_id}
          self.rendement_actu = self.K/self.K_initial
          dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
          self.trader_balance_sheet.append(dico)
          self.val=False
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet

class Trader_aleatoire:

  def __init__(self, K, pnl, nb_actions):
    self.K = K
    self.K_initial = self.K 
    self.pnl = pnl
    self.nb_actions = nb_actions
    self.trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
    self.trader_balance_sheet = []
    self.rendement_actu = self.K/self.K_initial
    quote = {'type' : np.nan, 
               'side' : np.nan, 
               'quantity' : np.nan, 
               'price' : np.nan,
               'trade_id' : self.trade_id}
    dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
    self.trader_balance_sheet.append(dico)
    self.val = False

  def trade(self, order_book):
    x = np.random.randint(0,2)
    if x == 0 and self.K >= 0:
      type_order = 'market'
      self.side = 'ask'
      quantity = max(self.K/order_book.get_best_ask(),0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        quote = {'type': type_order,
                  'side': self.side,
                  'quantity': quantity,
                  'trade_id': self.trade_id}
        self.K -= quantity*order_book.get_best_ask()
        self.pnl -= quantity*order_book.get_best_ask()
        self.nb_actions += quantity
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    elif x == 1 and self.nb_actions > 0:
      type_order = 'market'
      self.side = 'bid'
      quantity = max(self.nb_actions-1,0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        quote = {'type': type_order,
                  'side': self.side,
                  'quantity': quantity,
                  'trade_id': self.trade_id}
        self.K += quantity*order_book.get_best_bid()
        self.pnl += quantity*order_book.get_best_bid()
        self.nb_actions -= quantity
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet

class Trader_haussier:
  #Ce trader pense qu'il pourra vendre très chere donc il va acheter en market order puis va envoyer un ordre lim de vente au pire des Bids
  def __init__(self, K, pnl, nb_actions):
    self.K = K
    self.K_initial = self.K
    self.nb_actions = nb_actions 
    self.pnl = pnl
    self.trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
    self.trader_balance_sheet = []
    self.rendement_actu = self.K/self.K_initial
    quote = {'type' : np.nan, 
               'side' : np.nan, 
               'quantity' : np.nan, 
               'price' : np.nan,
               'trade_id' : self.trade_id}
    dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
    self.trader_balance_sheet.append(dico)
    self.val=False

  def tradeFirst(self, order_book):
     type_order = 'market'
     self.side = 'ask'
     quantity = max(self.K/order_book.get_best_ask(),0)
     if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
     else:
        quote = {'type': type_order,
                  'side': self.side,
                  'quantity': quantity,
                  'trade_id': self.trade_id}
        self.K -= quantity*order_book.get_best_ask()
        self.pnl -= quantity*order_book.get_best_ask()
        self.nb_actions += quantity
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
     return self.val, quote, self.trader_balance_sheet
  
  def SecondTrade(self, order_book):
    if self.nb_actions>0:
      worst_bid = order_book.get_worst_bid() 
      type_order = 'limit'
      self.side = 'bid'
      quantity = max(self.nb_actions-1,0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        quote = {'type' : type_order, 
                'side' : self.side, 
                'quantity' : quantity, 
                'price' : worst_bid,
                'trade_id' : self.trade_id}
        self.K += quantity*worst_bid
        self.pnl += quantity*worst_bid
        self.rendement_actu = self.K/self.K_initial
        self.nb_actions -= quantity
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet

class Trader_baissier:
  #Ce dernier c'est l'inverse du dernier il dispose dejà d'actions et il pense qu'il pourra les racheter à pas chère du tout
  def __init__(self, K, pnl, nb_actions):
    self.K = K
    self.K_initial = self.K
    self.nb_actions = nb_actions 
    self.pnl = pnl
    self.trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
    self.trader_balance_sheet = []
    self.rendement_actu = self.K/self.K_initial
    quote = {'type' : np.nan, 
               'side' : np.nan, 
               'quantity' : np.nan, 
               'price' : np.nan,
               'trade_id' : self.trade_id}
    dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
    self.trader_balance_sheet.append(dico)
    self.val = False

  def tradeFirst(self, order_book):
    if self.nb_actions>0:
      type_order = 'market'
      self.side = 'bid'
      quantity = max(self.nb_actions-1,0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        quote = {'type': type_order,
                  'side': self.side,
                  'quantity': quantity,
                  'trade_id': self.trade_id}
        self.K += quantity*order_book.get_best_ask()
        self.pnl += quantity*order_book.get_best_ask()
        self.nb_actions -= quantity
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet
  
  def SecondTrade(self, order_book):
    if self.nb_actions==0:
      worst_ask = order_book.get_worst_ask() 
      type_order = 'limit'
      self.side = 'ask'
      quantity = max(self.K/order_book.get_worst_ask()-1,0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        quote = {'type' : type_order, 
                'side' : self.side, 
                'quantity' : quantity, 
                'price' : worst_ask,
                'trade_id' : self.trade_id}
        self.K -= quantity*worst_ask
        self.pnl -= quantity*worst_ask
        self.rendement_actu = self.K/self.K_initial
        self.nb_actions += quantity
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet
    
  def ThirdTrade(self, order_book):
    if self.nb_actions>0:
      worst_bid = order_book.get_worst_bid() 
      type_order = 'limit'
      self.side = 'bid'
      quantity = max(self.nb_actions,0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        quote = {'type' : type_order, 
                'side' : self.side, 
                'quantity' : quantity, 
                'price' : worst_bid,
                'trade_id' : self.trade_id}
        self.K += quantity*worst_bid
        self.pnl += quantity*worst_bid
        self.rendement_actu = self.K/self.K_initial
        self.nb_actions -= quantity
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet

class Trader_MA:
  #Ce trader va prendre la Moyenne mobile à n jours des trades prix des trades et va par la suite regarder le moment ou ou le prix du dernier trade passe en dessous de cette MA(n) il vendera
  #il enverra un ordre limite de vente adapté pour ne rien perdre pour chercher ainsi la meilleur éxecution et inversement si le prix du dernier trade passe au dessus de cette MA(n) il achetera
  def __init__(self, K, pnl, nb_actions, n):
    self.val = False
    self.K = K
    self.K_initial = self.K
    self.nb_actions = nb_actions 
    self.pnl = pnl
    self.n = n
    self.trade_id = 1000*np.random.randint(1,10) + 100*np.random.randint(1,10) + 10*np.random.randint(1,10) + np.random.randint(1,10)
    self.trader_balance_sheet = []
    self.rendement_actu = self.K/self.K_initial
    quote = {'type' : np.nan, 
               'side' : np.nan, 
               'quantity' : np.nan, 
               'price' : np.nan,
               'trade_id' : self.trade_id}
    dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
    self.trader_balance_sheet.append(dico)
  
  def firstTrade(self, order_book):
    mva_order = self.n
    bids, asks, trades_done = order_book.get_all()
    prices_trades = [x['prix'] for x in trades_done[:-1]]
    mva_avg = mvt_avg(prices_trades, mva_order)
    if prices_trades[-1] > mva_avg[-1] and self.K > 0:
      type_order = 'limit'
      self.side = 'ask'
      quantity = max(min(self.K/order_book.get_best_ask()-1, order_book.get_volume_at_price('ask',order_book.get_best_ask())),0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        price = order_book.get_best_ask()
        quote = {'type' : type_order, 
                'side' : self.side, 
                'quantity' : quantity, 
                'price' : price,
                'trade_id' : self.trade_id}
        self.K -= price*quantity
        self.pnl -= price*quantity
        self.nb_actions += quantity
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    elif prices_trades[-1] < mva_avg[-1] and self.nb_actions > 0:
      type_order = 'limit'
      self.side = 'bid'
      quantity = max(self.nb_actions-1,0)
      if quantity<=0:
        quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=False
      else:
        price = order_book.get_best_bid()
        quote = {'type' : type_order, 
                'side' : self.side, 
                'quantity' : quantity, 
                'price' : price,
                'trade_id' : self.trade_id}
        self.K += price*quantity
        self.pnl += price*quantity
        self.nb_actions -= quantity
        self.rendement_actu = self.K/self.K_initial
        dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
        self.trader_balance_sheet.append(dico)
        self.val=True
    else:
      quote = {'type' : np.nan, 
                'side' : np.nan, 
                'quantity' : np.nan, 
                'price' : np.nan,
                'trade_id' : self.trade_id}
      self.rendement_actu = self.K/self.K_initial
      dico = {'Capital Courant' : self.K, 'Pnl Cumulé' : self.pnl,'Rendement Actuelle Brute' : self.rendement_actu, 'nb_actions' : self.nb_actions,'ordre_envoyé' : quote}
      self.trader_balance_sheet.append(dico)
      self.val=False
    return self.val, quote, self.trader_balance_sheet


def GetStats(Balancesheet,nom_strat_trader, order_book, all_trades):
  
  cap_courant = []
  pnl_cum = []
  rdm_act_brute = []
  
  for i in range(len(Balancesheet)):
    cap_courant.append(float(Balancesheet[i]['Capital Courant']))
    pnl_cum.append(float(Balancesheet[i]['Pnl Cumulé']))
    rdm_act_brute.append(float(Balancesheet[i]['Rendement Actuelle Brute']))
  
  all_trades = [float(x) for x in all_trades]
  trades_df = pd.DataFrame(list(zip(list(np.arange(len(all_trades))), all_trades)), columns = ['Ordre de trades', 'Prix des trades'])
  mean_cap_courant = np.mean(cap_courant)
  std_cap_courant = np.std(cap_courant)
  min_cap_courant = np.min(cap_courant)
  max_cap_courant = np.max(cap_courant)
  q1_cap_courant = np.quantile(cap_courant, 0.25)
  q2_cap_courant = np.quantile(cap_courant, 0.5)
  q3_cap_courant = np.quantile(cap_courant, 0.75)
  Var_cap_courant = np.quantile(cap_courant, 0.95)
  count = len(cap_courant)
  df_stats_cap_courant = pd.DataFrame([count, mean_cap_courant, std_cap_courant, min_cap_courant, max_cap_courant,q1_cap_courant,q2_cap_courant,q3_cap_courant, Var_cap_courant],
                                      columns=['Statistique descriptives Capital Courant pour la strat: {}'.format(nom_strat_trader)],
                                      index=['count', 'Moyenne', 'Ecart-type', 'Min', 'Max', '1er quartile', 'médiane', '3ème quartile', '95ème quantile(VAR)'])
  
  mean_pnl_cum = np.mean(pnl_cum)
  std_pnl_cum = np.std(pnl_cum)
  min_pnl_cum = np.min(pnl_cum)
  max_pnl_cum = np.max(pnl_cum)
  q1_pnl_cum = np.quantile(pnl_cum, 0.25)
  q2_pnl_cum = np.quantile(pnl_cum, 0.5)
  q3_pnl_cum = np.quantile(pnl_cum, 0.75)
  Var_pnl_cum = np.quantile(pnl_cum, 0.95)
  count = len(pnl_cum)
  df_stats_pnl_cum = pd.DataFrame([count, mean_pnl_cum, std_pnl_cum, min_pnl_cum, max_pnl_cum,q1_pnl_cum,q2_pnl_cum,q3_pnl_cum, Var_pnl_cum],
                                      columns=['Statistique descriptives Pnl Cumulé pour la strat: {}'.format(nom_strat_trader)],
                                      index=['count', 'Moyenne', 'Ecart-type', 'Min', 'Max', '1er quartile', 'médiane', '3ème quartile', '95ème quantile(VAR)'])
  
  mean_rdm_act_brute = np.mean(rdm_act_brute)
  std_rdm_act_brute = np.std(rdm_act_brute)
  min_rdm_act_brute = np.min(rdm_act_brute)
  max_rdm_act_brute = np.max(rdm_act_brute)
  count = len(rdm_act_brute)
  q1_rdm_act_brute = np.quantile(rdm_act_brute, 0.25)
  q2_rdm_act_brute = np.quantile(rdm_act_brute, 0.5)
  q3_rdm_act_brute = np.quantile(rdm_act_brute, 0.75)
  Var_rdm_act_brute = np.quantile(rdm_act_brute, 0.95)
  df_stats_rdm_act_brute = pd.DataFrame([count, mean_rdm_act_brute, std_rdm_act_brute, min_rdm_act_brute, max_rdm_act_brute,q1_rdm_act_brute,q2_rdm_act_brute,q3_rdm_act_brute, Var_rdm_act_brute],
                                      columns=['Statistique descriptives Rendement Actuelle Brute pour la strat: {}'.format(nom_strat_trader)],
                                      index=['count', 'Moyenne', 'Ecart-type', 'Min', 'Max', '1er quartile', 'médiane', '3ème quartile', '95ème quantile(VAR)'])
  
  mean_all_trades = np.mean(all_trades)
  std_all_trades = np.std(all_trades)
  min_all_trades = np.min(all_trades)
  max_all_trades = np.max(all_trades)
  count = len(all_trades)
  q1_all_trades = np.quantile(all_trades, 0.25)
  q2_all_trades = np.quantile(all_trades, 0.5)
  q3_all_trades = np.quantile(all_trades, 0.75)
  Var_all_trades = np.quantile(all_trades, 0.95)
  df_stats_all_trades = pd.DataFrame([count, mean_all_trades, std_all_trades, min_all_trades, max_all_trades, q1_all_trades, q2_all_trades, q3_all_trades, Var_all_trades],
                                      columns=['Statistique descriptives Capital Courant pour la strat: {}'.format(nom_strat_trader)],
                                      index=['count', 'Moyenne', 'Ecart-type', 'Min', 'Max', '1er quartile', 'médiane', '3ème quartile', '95ème quantile(VAR)'])
  
  return df_stats_cap_courant, df_stats_pnl_cum, df_stats_rdm_act_brute, trades_df, cap_courant, pnl_cum, rdm_act_brute 


def GetList(traders, nom_strat_trader, trajecs):
    
    for Balancesheet, j in zip(traders, range(len(traders))):
      cap_courant = []
      pnl_cum = []
      rdm_act_brute = []
      trajec = []
      
      for i in range(len(Balancesheet)):
        cap_courant.append(float(Balancesheet[i]['Capital Courant']))
        pnl_cum.append(float(Balancesheet[i]['Pnl Cumulé']))
        rdm_act_brute.append(float(Balancesheet[i]['Rendement Actuelle Brute']))
      
      for i in range(len(trajecs[j])):
        trajec.append(float(trajecs[j][i]))
      cap_courant = np.array(cap_courant)
      pnl_cum = np.array(pnl_cum)
      rdm_act_brute = np.array(rdm_act_brute)
      
      if j==0:
        df_cap_courant = pd.DataFrame(cap_courant, columns=["trader "+str(j)+' '+nom_strat_trader])
        df_pnl_cum = pd.DataFrame(pnl_cum, columns=["trader "+str(j)+' '+nom_strat_trader])
        df_rdm_act_brute = pd.DataFrame(rdm_act_brute, columns=["trader "+str(j)+' '+nom_strat_trader])
        df_trajec = pd.DataFrame(trajec, columns=["trajectoires "+str(j)+' '+nom_strat_trader])
      
      else:
        df_cap_courant["trader "+str(j)+' '+nom_strat_trader] = cap_courant
        df_pnl_cum["trader "+str(j)+' '+nom_strat_trader] = pnl_cum
        df_rdm_act_brute["trader "+str(j)+' '+nom_strat_trader] = rdm_act_brute
        df_trajec = pd.DataFrame(trajec, columns=["trajectoires "+str(j)+' '+nom_strat_trader])
    GetVisualization2(df_cap_courant, df_pnl_cum, df_rdm_act_brute,df_trajec, nom_strat_trader)

def GetVisualization2(df_cap_courant, df_pnl_cum, df_rdm_act_brute,df_trajec, nom_strat_trader):
  fig=plt.figure(figsize=(20,10))
  fig1=fig.add_subplot(221)
  df_pnl_cum.plot(ax=plt.gca(), legend=False, title=f'Pnl Cumulés Stratégie : {nom_strat_trader}')
  fig2=fig.add_subplot(222)
  df_rdm_act_brute.plot(ax=plt.gca(), legend=False, title=f'Rendement Brute Stratégie : {nom_strat_trader}')
  fig3=fig.add_subplot(2,2,3)
  df_cap_courant.plot(ax=plt.gca(), legend=False, title=f'Capital Courant Stratégie : {nom_strat_trader}')
  fig4=fig.add_subplot(224)
  df_trajec.plot(ax=plt.gca(), legend=False, title=f'Trades Stratégie : {nom_strat_trader}')
  plt.show()

nb_ordre_depart = int(input("Veuillez Précisez le nombre d'ordre limite de départ : "))

price_range_bid_min = int(input("Veuillez précisez le prix minimale pour les Bids : "))

price_range_bid_max = int(input("Veuillez précisez le prix maximale pour les Bids : "))

price_range_ask_min = int(input("Veuillez précisez le prix minimale pour les Asks : "))

price_range_ask_max = int(input("Veuillez précisez le prix maximale pour les Asks : "))

qte_range_ask_min = int(input("Veuillez précisez la quantité minimale par Ask : "))

qte_range_ask_max = int(input("Veuillez précisez la quantité maximale par Ask : "))

qte_range_bid_min = int(input("Veuillez précisez la quantité minimale par Bid : "))

qte_range_bid_max = int(input("Veuillez précisez la quantité maximale par Bid : "))


orders = generate_lim_orders(nb_ordre_depart, [price_range_bid_min,price_range_bid_max], [price_range_ask_min,price_range_ask_max], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])

trajecs = []
trader_qte = []
trader_buy_and_sell = []
dist_fin_trader_qte = []
trader_aleatoire = []
trader_haussier = []
trader_baissier = []
all_trajecs = []
trader_MA = []
dist_fin_trader_buy_and_sell = []
dist_fin_trader_aleatoire = []
dist_fin_trader_haussier = []
dist_fin_trader_baissier = []
dist_fin_trader_MA = []

order_book = OrderBook()

for order in orders:
    trades, order_id = order_book.process_order(order, False, False)

nb_transac_times = int(input("Veuillez précisez le nombre fois que nos traders pouront faire des transactions : "))

nb_trader_par_strat = int(input("Veuillez précisez le nombre de Trader par transaction"))

K_trader_qte = int(input("Veuillez préciser le capital initial de Trader_quantity : "))

pnl_trader_qte = int(input("Veuillez précisez le pnl de départ de Trader_quantity : "))

nb_act_trader_qte = int(input("Veuillez précisez le nombre d'actions détenus initialement par Trader_quantity : "))

K_trader_aleatoire = int(input("Veuillez préciser le capital initial de Trader_aleatoire : "))

pnl_trader_aleatoire = int(input("Veuillez précisez le pnl de départ de Trader_aleatoire : "))

nb_act_trader_aleatoire = int(input("Veuillez précisez le nombre d'actions détenus initialement par Trader_aleatoire : "))

K_trader_haussier = int(input("Veuillez préciser le capital initial de Trader_haussier : "))

pnl_trader_haussier = int(input("Veuillez précisez le pnl de départ de Trader_haussier : "))

nb_act_trader_haussier = int(input("Veuillez précisez le nombre d'actions détenus initialement par Trader_haussier : "))

K_trader_baissier = int(input("Veuillez préciser le capital initial de Trader_baissier : "))

pnl_trader_baissier = int(input("Veuillez précisez le pnl de départ de Trader_baissier : "))

nb_act_trader_baissier =int(input("Veuillez précisez le nombre d'actions détenus initialement par Trader_baissier : "))

K_trader_MA = int(input("Veuillez préciser le capital initial de Trader_MA : "))

pnl_trader_MA = int(input("Veuillez précisez le pnl de départ de Trader_MA : "))

nb_act_trader_MA = int(input("Veuillez précisez le nombre d'actions détenus initialement par Trader_MA : "))

mvg_trader_MA = int(input("Veuillez précisez l'ordre de la moyenne mobile à retenir : "))

for n in range(nb_trader_par_strat):
  
  all_trades = []
  exec(f'T{n}_qte = Trader_quantity(K_trader_qte, pnl_trader_qte, nb_act_trader_qte)')
  exec(f'T{n}_buy_and_sell = Trader_Buy_and_sell(order_book)')
  exec(f'T{n}_aleatoire = Trader_aleatoire(K_trader_aleatoire, pnl_trader_aleatoire,nb_act_trader_aleatoire)')
  exec(f'T{n}_haussier = Trader_haussier(K_trader_haussier, pnl_trader_haussier, nb_act_trader_haussier)')
  exec(f'T{n}_baissier = Trader_baissier(K_trader_baissier, pnl_trader_baissier, nb_act_trader_baissier)')
  exec(f'T{n}_MA = Trader_MA(K_trader_MA, pnl_trader_MA, nb_act_trader_MA, mvg_trader_MA)')
  bids, asks, trades_done = order_book.get_all()
  all_trades.append([x['prix'] for x in trades_done][-1])
  for nb in np.arange(nb_transac_times):
    
    exec(f'val, quote1_T{n}_qte, bs_T{n}_qte = T{n}_qte.trade_first(order_book)')
    if val == True:
      exec(f'order_book.process_order(quote1_T{n}_qte, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1]) 
      orders = generate_lim_orders(5, [price_range_bid_min+5,price_range_bid_max+5], [price_range_ask_min,price_range_ask_max], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote2_T{n}_qte, bs_T{n}_qte = T{n}_qte.tradeSecond(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote2_T{n}_qte, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote_T{n}_buy_and_sell, bs_T{n}_buy_and_sell = T{n}_buy_and_sell.trade(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote_T{n}_buy_and_sell, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
      orders = generate_lim_orders(5, [price_range_bid_min+5,price_range_bid_max+5], [price_range_ask_min+6,price_range_ask_max+5], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote_T{n}_aleatoire, bs_T{n}_aleatoire = T{n}_aleatoire.trade(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote_T{n}_aleatoire, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])  
    exec(f'val,quote1_T{n}_baissier, bs_T{n}_baissier = T{n}_baissier.tradeFirst(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote1_T{n}_baissier, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
      orders = generate_lim_orders(2, [price_range_bid_min-5,price_range_bid_max-3], [price_range_ask_min-3,price_range_ask_max-5], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote2_T{n}_baissier, bs_T{n}_baissier = T{n}_baissier.SecondTrade(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote2_T{n}_baissier, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
      orders = generate_lim_orders(5, [price_range_bid_min+5,price_range_bid_max+5], [price_range_ask_min+7,price_range_ask_max+10], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote3_T{n}_baissier, bs_T{n}_baissier = T{n}_baissier.ThirdTrade(order_book)')
    if val == True:
      exec(f'order_book.process_order(quote3_T{n}_baissier, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])  
    exec(f'val,quote1_T{n}_haussier, bs_T{n}_haussier = T{n}_haussier.tradeFirst(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote1_T{n}_haussier, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
      orders = generate_lim_orders(5, [price_range_bid_min+5,price_range_bid_max+5], [price_range_ask_min+4,price_range_ask_max+4], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote2_T{n}_haussier, bs_T{n}_haussier = T{n}_haussier.SecondTrade(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote2_T{n}_haussier, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
      orders = generate_lim_orders(3, [price_range_bid_min-4,price_range_bid_max-4], [price_range_ask_min-2,price_range_ask_max-2], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
    exec(f'val,quote_T{n}_MA, bs_T{n}_MA = T{n}_MA.firstTrade(order_book)')
    
    if val == True:
      exec(f'order_book.process_order(quote_T{n}_MA, False, False)')
      bids, asks, trades_done = order_book.get_all()
      all_trades.append([x['prix'] for x in trades_done][-1])
      orders = generate_lim_orders(2, [price_range_bid_min+1,price_range_bid_max+1], [price_range_ask_min+1,price_range_ask_max+2], [qte_range_ask_min,qte_range_ask_max], [qte_range_bid_min,qte_range_bid_max])
      for order in orders:
        trades, order_id = order_book.process_order(order, False, False)
        bids, asks, trades_done = order_book.get_all()
        all_trades.append([x['prix'] for x in trades_done][-1])
  
  exec(f'dist_fin_trader_qte.append(bs_T{n}_qte[-1])')
  exec(f'dist_fin_trader_buy_and_sell.append(bs_T{n}_buy_and_sell[-1])')
  exec(f'dist_fin_trader_aleatoire.append(bs_T{n}_aleatoire[-1])')
  exec(f'dist_fin_trader_haussier.append(bs_T{n}_haussier[-1])')
  exec(f'dist_fin_trader_baissier.append(bs_T{n}_baissier[-1])')
  exec(f'dist_fin_trader_MA.append(bs_T{n}_MA[-1])')
  trajecs.append(all_trades[-1])
  exec(f'trader_qte.append(bs_T{n}_qte)')
  exec(f'trader_buy_and_sell.append(bs_T{n}_buy_and_sell)')
  exec(f'trader_aleatoire.append(bs_T{n}_aleatoire)')
  exec(f'trader_haussier.append(bs_T{n}_haussier)')
  exec(f'trader_baissier.append(bs_T{n}_baissier)')
  exec(f'trader_MA.append(bs_T{n}_MA)')
  all_trajecs.append(all_trades)

#On visualise les différentes simulations et leurs trajectoires pour différentes Stratégies 
GetList(trader_qte, "Trader_quantité", all_trajecs)
GetList(trader_buy_and_sell, "Trader_Buy_and_sell", all_trajecs)
GetList(trader_aleatoire, "Trader_aleatoire", all_trajecs)
GetList(trader_haussier, "Trader_haussier", all_trajecs)
GetList(trader_baissier, "Trader_baissier", all_trajecs)
GetList(trader_MA, "Trader_MA", all_trajecs)

df_stats_cap_courant_trader_qte, df_stats_pnl_cum_trader_qte, df_stats_rdm_act_brute_trader_qte, trades_df, cap_courant_trader_qte, pnl_cum_trader_qte, rdm_act_brute_trader_qte = GetStats(dist_fin_trader_qte,"Trader_quantity", order_book, trajecs)
df_stats_cap_courant_trader_Buy_and_sell, df_stats_pnl_cum_Buy_and_sell, df_stats_rdm_act_brute_Buy_and_sell, trades_df, cap_courant_Buy_and_sell, pnl_cum_Buy_and_sell, rdm_act_brute_Buy_and_sell = GetStats(dist_fin_trader_buy_and_sell,"Trader_Buy_and_sell", order_book, trajecs)
df_stats_cap_courant_trader_aleatoire, df_stats_pnl_cum_trader_aleatoire, df_stats_rdm_act_brute_trader_aleatoire, trades_df, cap_courant_trader_aleatoire, pnl_cum_trader_aleatoire, rdm_act_brute_trader_aleatoire = GetStats(dist_fin_trader_aleatoire,"trader_aleatoire", order_book, trajecs)
df_stats_cap_courant_trader_haussier, df_stats_pnl_cum_trader_haussier, df_stats_rdm_act_brute_trader_haussier, trades_df, cap_courant_trader_haussier, pnl_cum_trader_haussier, rdm_act_brute_trader_haussier = GetStats(dist_fin_trader_haussier,"trader_haussier", order_book, trajecs)
df_stats_cap_courant_trader_baissier, df_stats_pnl_cum_trader_baissier, df_stats_rdm_act_brute_trader_baissier, trades_df, cap_courant_trader_baissier, pnl_cum_trader_baissier, rdm_act_brute_trader_baissier = GetStats(dist_fin_trader_baissier,"trader_baissier", order_book, trajecs)
df_stats_cap_courant_trader_MA, df_stats_pnl_cum_trader_MA, df_stats_rdm_act_brute_trader_MA, trades_df, cap_courant_trader_MA, pnl_cum_trader_MA, rdm_act_brute_trader_MA = GetStats(dist_fin_trader_MA,"trader_MA", order_book, trajecs)

print(f"Statistiques Descriptives de fin de période sur {nb_trader_par_strat} simulations faite avec la stratégie Trader_quantité avec les paramètres spécifiés : ")
Df_Trader_qte = pd.concat([df_stats_cap_courant_trader_qte,df_stats_pnl_cum_trader_qte,df_stats_rdm_act_brute_trader_qte], axis=1, ignore_index=True)
Df_Trader_qte.columns = ['Capital Courant', 'Pnl Cumulé', 'Rendement Brute']
print(Df_Trader_qte)
writer = pd.ExcelWriter(f'Statistiques de fin de période avec la stratégie Trader Quantité sur {nb_trader_par_strat} simulations.xlsx')
Df_Trader_qte.to_excel(writer)
writer.save()
print("###################")
print("Statistiques Descriptives de fin de période sur {} simulations faite avec la stratégie Trader_Buy_and_sell avec les paramètres spécifiés : ".format(nb_trader_par_strat))
Df_trader_Buy_and_sell = pd.concat([df_stats_cap_courant_trader_Buy_and_sell,df_stats_pnl_cum_Buy_and_sell,df_stats_rdm_act_brute_Buy_and_sell], axis=1, ignore_index=True)
Df_trader_Buy_and_sell.columns = ['Capital Courant', 'Pnl Cumulé', 'Rendement Brute']
print(Df_trader_Buy_and_sell)
writer = pd.ExcelWriter(f'Statistiques de fin de période avec la stratégie Trader Buy and Sell sur {nb_trader_par_strat} simulations.xlsx')
Df_trader_Buy_and_sell.to_excel(writer)
writer.save()
print("##################")
print("Statistiques Descriptives de fin de période sur {} simulations faite avec la stratégie Trader_aleatoire avec les paramètres spécifiés : ".format(nb_trader_par_strat))
Df_trader_trader_aleatoire = pd.concat([df_stats_cap_courant_trader_aleatoire,df_stats_pnl_cum_trader_aleatoire,df_stats_rdm_act_brute_trader_aleatoire], axis=1, ignore_index=True)
Df_trader_trader_aleatoire.columns = ['Capital Courant', 'Pnl Cumulé', 'Rendement Brute']
print(Df_trader_trader_aleatoire)
writer = pd.ExcelWriter(f'Statistiques de fin de période avec la stratégie Trader Aleatoire sur {nb_trader_par_strat} simulations.xlsx')
Df_trader_trader_aleatoire.to_excel(writer)
writer.save()
print("##################")
print("Statistiques Descriptives de fin de période sur {} simulations faite avec la stratégie Trader_haussier avec les paramètres spécifiés : ".format(nb_trader_par_strat))
Df_trader_trader_haussier = pd.concat([df_stats_cap_courant_trader_haussier,df_stats_pnl_cum_trader_haussier,df_stats_rdm_act_brute_trader_haussier], axis=1, ignore_index=True)
Df_trader_trader_haussier.columns = ['Capital Courant', 'Pnl Cumulé', 'Rendement Brute']
print(Df_trader_trader_haussier)
writer = pd.ExcelWriter(f'Statistiques de fin de période avec la stratégie Trader Haussier sur {nb_trader_par_strat} simulations.xlsx')
Df_trader_trader_haussier.to_excel(writer)
writer.save()
print("##############")
print("Statistiques Descriptives de fin de période sur {} simulations faite avec la stratégie Trader_baissier avec les paramètres spécifiés : ".format(nb_trader_par_strat))
Df_trader_trader_baissier = pd.concat([df_stats_cap_courant_trader_baissier,df_stats_pnl_cum_trader_baissier,df_stats_rdm_act_brute_trader_baissier], axis=1, ignore_index=True)
Df_trader_trader_baissier.columns = ['Capital Courant', 'Pnl Cumulé', 'Rendement Brute']
print(Df_trader_trader_baissier)
writer = pd.ExcelWriter(f'Statistiques de fin de période avec la stratégie Trader Baissier sur {nb_trader_par_strat} simulations.xlsx')
Df_trader_trader_baissier.to_excel(writer)
writer.save()
print('############')
print("Statistiques Descriptives de fin de période sur {} simulations faite avec la stratégie Trader_MA avec les paramètres spécifiés : ".format(nb_trader_par_strat))
Df_trader_trader_MA = pd.concat([df_stats_cap_courant_trader_MA,df_stats_pnl_cum_trader_MA,df_stats_rdm_act_brute_trader_MA], axis=1, ignore_index=True)
Df_trader_trader_MA.columns = ['Capital Courant', 'Pnl Cumulé', 'Rendement Brute']
print(Df_trader_trader_MA)
writer = pd.ExcelWriter(f'Statistiques de fin de période avec la stratégie Trader MA sur {nb_trader_par_strat} simulations.xlsx')
Df_trader_trader_MA.to_excel(writer)
writer.save()
```