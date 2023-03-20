import React from 'react'
import AuthorList from './components/Author.js'
import BookList from './components/Book.js'
import AuthorBookList from './components/AuthorBook.js'
import LoginForm from './components/Auth.js'
import BookForm from './components/BookForm.js'

import { BrowserRouter, Route, Switch, Redirect, Link } from 'react-router-dom'
import axios from 'axios'
import Cookies from 'universal-cookie';
const NotFound404 = ({ location }) => {
  return (
    <div>
      <h1>Страница по адресу '{location.pathname}' не найдена</h1>
    </div>
  )
}
class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      'authors': [],
      'books': [],
      'token': ''
    }
  }
  set_token(token) {
    const cookies = new Cookies()
    cookies.set('token', token)
    this.setState({ 'token': token }, () => this.load_data())
  }
  is_authenticated() {
    return this.state.token != ''
  }
  logout() {
    this.set_token('')
  }
  get_token_from_storage() {
    const cookies = new Cookies()
    const token = cookies.get('token')
    this.setState({ 'token': token }, () => this.load_data())

  }
  get_token(username, password) {
    axios.post('http://127.0.0.1:8000/api-token-auth/', {
      username: username,
      password: password
    })
      .then(response => {
        this.set_token(response.data['token'])
      }).catch(error => alert('Неверный логин или пароль'))
  }
  get_headers() {
    let headers = {
      'Content-Type': 'application/json'
    }
    if (this.is_authenticated()) {
      headers['Authorization'] = 'Token ' + this.state.token
    }
    return headers
  }

  deleteBook(id) {
    const headers = this.get_headers()
    axios.delete(`http://127.0.0.1:8000/api/books/${id}`, { headers, headers })
      .then(response => {
        this.setState({
          books: this.state.books.filter((item) => item.id !==
            id)
        })
      }).catch(error => console.log(error))
  }


  load_data() {
    const headers = this.get_headers()
    axios.get('http://127.0.0.1:8000/api/authors/', { headers })
      .then(response => {
        this.setState({ authors: response.data })
      }).catch(error => console.log(error))
    axios.get('http://127.0.0.1:8000/api/books/', { headers })
      .then(response => {
        this.setState({ books: response.data })
      }).catch(error => {
        console.log(error)
        this.setState({ books: [] })
      })
  }
  componentDidMount() {
    this.get_token_from_storage()
  }
  createBook(name, author) {
    const headers = this.get_headers()
    const data = { name: name, author: author }
    axios.post(`http://127.0.0.1:8000/api/books/`, data, { headers, headers })
      .then(response => {
        let new_book = response.data
        const author = this.state.authors.filter((item) => item.id ===
          new_book.author)[0]
        new_book.author = author
        this.setState({ books: [...this.state.books, new_book] })
      }).catch(error => console.log(error))
  }
  render() {
    return (
      <div className="App">
        <BrowserRouter>
          <nav>
            <ul>
              <li>
                <Link to='/'>Authors</Link>
              </li>
              <li>
                <Link to='/books'>Books</Link>
              </li>
              <li>
                {this.is_authenticated() ? <button
                  onClick={() => this.logout()}>Logout</button> : <Link to='/login'>Login</Link>}
              </li>
            </ul>
          </nav>
          <Switch>
            <Route exact path='/' component={() => <AuthorList
              items={this.state.authors} />} />
            <Route exact path='/books' component={() => <BookList
              items={this.state.books} />} />
            <Route exact path='/login' component={() => <LoginForm
              get_token={(username, password) => this.get_token(username, password)} />} />
            <Route path="/author/:id">
              <AuthorBookList items={this.state.books} />
            </Route>
            <Redirect from='/authors' to='/' />
            <Route component={NotFound404} />
            <Route exact path='/books/create' component={() => <BookForm
              createBook={(name, author) => this.createBook(name, author)} />} />
            <Route exact path='/books/create' component={() => <BookForm />}
            />
            <Route exact path='/books' component={() => <BookList
              items={this.state.books} deleteBook={(id) => this.deleteBook(id)} />} />
          </Switch>
        </BrowserRouter>
      </div>
    )
  }
}
export default App