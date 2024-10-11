const modal = document.querySelector('.modal-container')
const tbody = document.querySelector('tbody')
const sNome = document.querySelector('#m-nome')
const sNumSerie = document.querySelector('#m-numserie')
const sStatus = document.querySelector('#m-status')
const sOS = document.querySelector('#m-OS')
const sCert = document.querySelector('#m-cert')
const sData = document.querySelector('#m-data')
const btnSalvar = document.querySelector('#btnSalvar')

let itens
let id

function openModal(edit = false, index = 0) {
 modal.classList.add('active')
 modal.onclick = e => {
   if (e.target.className.indexOf('modal-container') !== -1) {
     modal.classList.remove('active')
   }
 }
 if (edit) {
    sNome = itens[index].nome
    sNumSerie = itens[index].numserie
    sStatus = itens[index].status
    sOS = itens[index].OS
    sCert = itens[index].cert
    sData = itens[index].data
   id = index
 } else {
   sNome = ''
   sNumSerie=''
   sStatus = 'Ativo'
   sOS = ''
   sCert = ''
   sData = ''
 }
}
function editItem(index) {
 openModal(true, index)
}
function deleteItem(index) {
 itens.splice(index, 1)
 setItensBD()
 loadItens()
}
function insertItem(item, index) {
 let tr = document.createElement('tr')
 tr.innerHTML = `
<td>${item.nome}</td>
<td>${item.numserie}</td>
<td>${item.status}</td>
<td>${item.OS}</td>
<td>${item.cert}</td>
<td>${item.data}</td>
<td class="acao">
<button onclick="editItem(${index})"><i class='bx bx-edit' ></i></button>
</td>
<td class="acao">
<button onclick="deleteItem(${index})"><i class='bx bx-trash'></i></button>
</td>
 `
 tbody.appendChild(tr)
}
btnSalvar.onclick = e => {
    if (sNome.value == '' || sNumSerie.value == '' || sStatus.value == '' || sOS.value == '' || sCert.value == '' || sData.value == '') {
   return
 }
 e.preventDefault();
 if (id !== undefined) {
     itens[id].nome = sNome.value
     itens[id].numserie = sNumSerie.value
     itens[id].status = sStatus.value
     itens[id].OS = sOS.value
     itens[id].cert = sCert.value
     itens[id].data = sData.value
 } else {
     itens.push({'nome': sNome.value, 'numserie': sNumSerie.value, 'status': sStatus.value, 'OS': sOS.value, 'cert': sCert.value, 'data': sData.value})
 }
 setItensBD()
 modal.classList.remove('active')
 loadItens()
 id = undefined
}
function loadItens() {
 itens = getItensBD()
 tbody.innerHTML = ''
 itens.forEach((item, index) => {
   insertItem(item, index)
 })
}
const getItensBD = () => JSON.parse(localStorage.getItem('dbfunc')) ?? []
const setItensBD = () => localStorage.setItem('dbfunc', JSON.stringify(itens))
loadItens()