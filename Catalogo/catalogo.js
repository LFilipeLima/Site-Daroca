function produto_verdura(){
    
    let verdura= [aspargos,alcachofra,tomate]

    var produto={div:'<div class="Produto">',
    link:'<a href="/Pagina_Produto/produto.html"><button ></button>',
    titulo:'<h1>'+verdura+'</h1>', 
    imagem:'<img src="/Catalogo/'+verdura+'.png'+'alt="">',
    preco:'<h1>Preço:</h1>',
    num_preco:'<h1>17,99</h1>'}

    for (i in Range(0,3,1)){
    document.write(produto.div)
    document.write(produto.link)
    document.write(produto.titulo)
    document.write(produto.imagem)
    document.write(produto.preco)
    document.write(produto.num_preco)    
  }
    document.write('</a> </div>')
}
