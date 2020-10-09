import React from 'react';
import './App.css';
import 'rsuite/dist/styles/rsuite-default.css';
import {Container, Sidenav, Icon, Sidebar, Nav,  Header, Content} from 'rsuite';
import Executor from './Executor'
import Binaries from './Binaries'


class App extends React.Component {
  state = {
    page : 'executor',
    activeMenu: 1
  }
  render() {
    const { page, activeMenu } = this.state;
    return (
      <div className="sidebar-page">
        <Container>
          <Sidebar
            style={{ display: 'flex', flexDirection: 'column' }}
            width={260}
            collapsible
          >
            <Sidenav.Header>
              <div style={{

                padding: 18,
                fontSize: 16,
                height: 56,
                background: '#34c3ff',
                color: ' #fff',
                whiteSpace: 'nowrap',
                overflow: 'hidden'
                }}>
                <Icon icon="logo-analytics" size="lg" style={{ verticalAlign: 0 }} />
                <span style={{ marginLeft: 12 }}> TIDBCS</span>
              </div>
            </Sidenav.Header>
            <Sidenav
              expanded={true}
              appearance="subtle"
            >
              <Sidenav.Body>
                <Nav>
                  <Nav.Item eventKey="1" active={1===activeMenu} icon={<Icon icon="dashboard" />}
                    onClick={() => {
                      this.setState({page: 'executor', activeMenu: 1})}
                    }>
                    Executor
                  </Nav.Item>
                  <Nav.Item eventKey="2" active={2===activeMenu} icon={<Icon icon="list" />}
                    onClick={() => {
                      this.setState({page: 'binaries', activeMenu: 2})}
                    }>
                    Binaries
                  </Nav.Item>
                </Nav>
              </Sidenav.Body>
            </Sidenav>
          </Sidebar>

          <Container>
            <Header>
              <h2>
              {page === 'executor' && 'Executor'}
              {page === 'binaries' && 'Binaries'}
              </h2>
            </Header>
            <Content style={{
              padding: '20px',
              margin: '20px',
              background: '#fff'
              }}>
              {page === 'executor' && <Executor/>}
              {page === 'binaries' && <Binaries/>}
            </Content>
          </Container>
        </Container>
      </div>
    );
  }
}

export default App;
