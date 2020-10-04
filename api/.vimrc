source ~/.vimrc.d/coc.vimrc
source ~/.vimrc.d/snippets.vimrc
Plug 'tmhedberg/SimpylFold'
let g:SimpylFold_docstring_preview = 1

autocmd! filetype python nnoremap <F5> :call PythonRun()<cr>
function! PythonRun()
    execute "! python %"
endfunction

:set wildignore=*.pyc
set fdm=indent
