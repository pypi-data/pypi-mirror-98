from nuna.utils import *

class Nuna:
  def __init__(self, error=True):
    self.error = error
    self.stack = []

  def tokenize(self, code):
    com = '눈누난나주거!헤응💕흐읏'
    res = []
    cnt = scnt = qcnt = idx = column = lineno = 0
    st = Stream(code)

    while not st.isEOF():
      c = st.get()

      if c == '\n':
        lineno += 1; column = 0
        continue
      if self.error and c not in com:
        raise Exception(f'Invalid character "{c}" found. '
        f'(Line {lineno+1} Column {column+1}, Char {st.i})')

      g = st.get('흐으읏.')
      dotCtx = [['base', 0, 0, []]]

      while g:
        if g == '.': dotCtx[-1][1] += 1
        if g == '으': dotCtx[-1][2] += 1
        if g == '흐': dotCtx.append(['exp', 0, 0, []])
        if g == '읏': 
          last = dotCtx.pop()
          if dotCtx: dotCtx[-1][3] += [last]
          else: dotCtx.append(last)
          j = st.get('.')
          while j: j = st.get('.')
  
        g = st.get('흐으읏.')
      res.append([c, dotCtx[-1]])

      column += 1
      cnt = 0; scnt = 0
    return res
  
  def execute(self, code):
    result = ''
    tok = self.tokenize(code)
    for i in tok:
      com, ctx = i
      W = self.evaluate(ctx)
      if com in '눈누': self.push(W)
      if com in '난나': self.push(self.pop()*W)
      if com == '주': self.push(self.pop()-W)
      if com == '거': self.push(self.pop()+W)
      if com == '💕': self.push(self.pop()+self.pop())
      if com == '헤': self.pop()
      if com == '응': self.push(-(self.pop()-self.pop()))
      if com == '!':
        for i in self.stack:
          result += chr(i)
    stdout(result)
    return self.stack
  
  def pop(self):
    if self.stack: return self.stack.pop()
    return 0
  
  def getLast(self):
    if self.stack: return self.stack[-1]
    return 0
  
  def getSecondLast(self):
    if len(self.stack)>1: return self.stack[-2]
    return 0
  
  def push(self, item):
    self.stack.append(item)
  
  def clear(self):
    self.stack = []
  
  def evaluate(self, ctx):
    typ, cnt, scnt, child = ctx
    nrml = cnt + scnt*self.getSecondLast()
    val = sum(map(self.evaluate, child)) + nrml
    wval = val + ((not val) and (not cnt))
    if typ == 'exp': return 1<<wval
    if typ == 'base': return wval

    
  
def generate(text):
  res = ''
  _targ = list(map(lambda v: ord(v), text))
  targ = []
  idx = 0
  while idx < len(_targ)-1:
    targ.append(_targ[idx+1]-_targ[idx])
    idx += 1
  
  first = True
  for i in [_targ[0]] + targ:
    if i == 0: res += '!'; continue
    if not first: res += '\n'

    intv = 0
    while len(Factorize(abs(i))) == 1 and abs(i) > 6:
      i -= sign(i); intv += 1

    l = abs(i)
    s = sign(i)
    f = Factorize(l)

    res += choice('눈누')
    t = f.get(2, 0)
    for i in f:
      if i == 2: continue
      for _ in [0]*f[i]:
        res += f'나{"."*i}'
        if t > 0:
          L = t != 1
          res += f'나흐{"."*(L*2)}읏{"."*rand(2,5)}'
          t -= L + 1
    while t > 0:
      L = t != 1
      res += f'나흐{"."*(L*2)}읏{"."*rand(2,5)}'
      t -= L + 1
    
    res += f'나주{"."*intv}거{"."*(2*intv)}{""if first else"응 💕"[s+1]}!'
    first = False
  return res