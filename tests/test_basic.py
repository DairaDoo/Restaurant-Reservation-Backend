def test_app_is_created(app):
    """Verifica que la app Flask se inicializa correctamente."""
    assert app is not None
    assert app.testing is True

def test_index_route(client):
    """Verifica que al menos devuelve 404 en / (ya que no definiste ruta raíz)."""
    response = client.get("/")
    assert response.status_code in [200, 404]
