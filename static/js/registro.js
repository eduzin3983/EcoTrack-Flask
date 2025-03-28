// Função para simular o envio do formulário e exibir feedback.
// Futuramente sera implementado o envio dos dados para o backend. Agora é so um exemplo de como seria a validação do formulário.
document.getElementById('registrarForm').addEventListener('submit', function(e) {
    e.preventDefault();
  
    const data = document.getElementById('data').value;
    const agua = document.getElementById('agua').value;
    const energia = document.getElementById('energia').value;
    const residuos = document.getElementById('residuos').value;
    const percentual = document.getElementById('percentual').value;
    const transporte = document.getElementById('transporte').value;
  
    if (!data || !agua || !energia || !residuos || !percentual || !transporte) {
      document.getElementById('feedback').innerText = 'Por favor, preencha todos os campos corretamente.';
      return;
    }
  
    document.getElementById('feedback').innerText = 'Dados registrados com sucesso!';
    
});