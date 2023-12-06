$(function () {
  $('#calculator-form').on('submit', function (event) {
    event.preventDefault();
    calculate();
  });
});

function calculate() {
  const firstNumber = $('#firstNumber').val();
  const secondNumber = $('#secondNumber').val();
  const operator = $('#operator').val();
  const expression = firstNumber + operator + secondNumber;

  $.ajax({
    url: 'api/calculate',
    method: 'POST',
    data: JSON.stringify({
      'expression': expression
    }),
    contentType: 'application/json',
    success: function (data) {
      $('#result').val(data.result);
    },
    error: function (err) {
      const data = JSON.parse(err.responseText);
      alert("Error: " + data.detail[0].msg);
      $('#calculator-form').trigger('reset');
    }
  });
}
