-- =============================================================================
-- Neovim Configuration with lazy.nvim
-- =============================================================================

-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- =============================================================================
-- OPTIONS
-- =============================================================================

vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

local opt = vim.opt

opt.number = true
opt.relativenumber = true
opt.expandtab = true
opt.shiftwidth = 2
opt.tabstop = 2
opt.softtabstop = 2
opt.smartindent = true
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true
opt.scrolloff = 8
opt.sidescrolloff = 8
opt.signcolumn = "yes"
opt.updatetime = 250
opt.termguicolors = true
opt.cursorline = true
opt.splitright = true
opt.splitbelow = true
opt.undofile = true
opt.wrap = false
opt.laststatus = 3  -- global statusline
opt.showmode = false
opt.history = 1000
opt.autowrite = true

-- =============================================================================
-- KEYMAPS
-- =============================================================================

local map = function(mode, lhs, rhs, opts)
  opts = opts or {}
  opts.silent = opts.silent ~= false
  vim.keymap.set(mode, lhs, rhs, opts)
end

-- Clear search highlight
map("n", "<Esc>", "<cmd>nohlsearch<cr>")

-- Save / quit
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save file" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })
map("n", "<leader>Q", "<cmd>qa<cr>", { desc = "Quit all" })

-- File explorer
map("n", "<leader>e", "<cmd>Neotree toggle<cr>", { desc = "File Explorer" })
map("n", "<leader>o", "<cmd>Neotree focus<cr>", { desc = "Focus Explorer" })

-- Window navigation (mirrors AeroSpace hjkl)
map("n", "<C-h>", "<C-w>h", { desc = "Window left" })
map("n", "<C-j>", "<C-w>j", { desc = "Window down" })
map("n", "<C-k>", "<C-w>k", { desc = "Window up" })
map("n", "<C-l>", "<C-w>l", { desc = "Window right" })

-- Window splits
map("n", "<leader>-", "<cmd>split<cr>", { desc = "Split horizontal" })
map("n", "<leader>|", "<cmd>vsplit<cr>", { desc = "Split vertical" })

-- Move lines in visual mode
map("v", "J", ":m '>+1<cr>gv=gv", { desc = "Move line down" })
map("v", "K", ":m '<-2<cr>gv=gv", { desc = "Move line up" })

-- Better indent in visual mode (stay in visual)
map("v", "<", "<gv")
map("v", ">", ">gv")

-- jj to escape insert mode
map("i", "jj", "<Esc>", { desc = "Exit insert mode" })

-- Buffer navigation
map("n", "<S-h>", "<cmd>bprevious<cr>", { desc = "Previous buffer" })
map("n", "<S-l>", "<cmd>bnext<cr>", { desc = "Next buffer" })
map("n", "<leader>bd", "<cmd>bdelete<cr>", { desc = "Delete buffer" })

-- Diagnostic navigation (replaces F2/NERDTree from old vimrc)
map("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
map("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
map("n", "<leader>d", vim.diagnostic.open_float, { desc = "Show diagnostic" })

-- =============================================================================
-- PLUGINS
-- =============================================================================

require("lazy").setup({

  -- -------------------------------------------------------------------------
  -- Colorscheme
  -- -------------------------------------------------------------------------
  {
    "Mofiqul/dracula.nvim",
    lazy = false,
    priority = 1000,
    config = function()
      require("dracula").setup({ transparent_bg = false })
      vim.cmd.colorscheme("dracula")
    end,
  },

  -- -------------------------------------------------------------------------
  -- Status line
  -- -------------------------------------------------------------------------
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {
      options = {
        theme = "dracula",
        globalstatus = true,
        component_separators = { left = "", right = "" },
        section_separators = { left = "", right = "" },
      },
      sections = {
        lualine_a = { "mode" },
        lualine_b = { "branch", "diff", "diagnostics" },
        lualine_c = { { "filename", path = 1 } },
        lualine_x = { "encoding", "filetype" },
        lualine_y = { "progress" },
        lualine_z = { "location" },
      },
    },
  },

  -- -------------------------------------------------------------------------
  -- File explorer
  -- -------------------------------------------------------------------------
  {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-tree/nvim-web-devicons",
      "MunifTanjim/nui.nvim",
    },
    opts = {
      filesystem = {
        filtered_items = {
          visible = true,
          hide_dotfiles = false,
          hide_gitignored = false,
        },
        follow_current_file = { enabled = true },
      },
      window = { width = 35 },
    },
  },

  -- -------------------------------------------------------------------------
  -- Fuzzy finder (pairs with fzf in shell)
  -- -------------------------------------------------------------------------
  {
    "nvim-telescope/telescope.nvim",
    branch = "0.1.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
    },
    keys = {
      { "<leader>ff", "<cmd>Telescope find_files<cr>",              desc = "Find files" },
      { "<leader>fg", "<cmd>Telescope live_grep<cr>",               desc = "Live grep" },
      { "<leader>fb", "<cmd>Telescope buffers<cr>",                 desc = "Buffers" },
      { "<leader>fh", "<cmd>Telescope help_tags<cr>",               desc = "Help tags" },
      { "<leader>fr", "<cmd>Telescope oldfiles<cr>",                desc = "Recent files" },
      { "<leader>fd", "<cmd>Telescope diagnostics<cr>",             desc = "Diagnostics" },
      { "<leader>fs", "<cmd>Telescope lsp_document_symbols<cr>",    desc = "Document symbols" },
      { "<leader>fw", "<cmd>Telescope lsp_workspace_symbols<cr>",   desc = "Workspace symbols" },
      { "<leader>gc", "<cmd>Telescope git_commits<cr>",             desc = "Git commits" },
      { "<leader>gb", "<cmd>Telescope git_branches<cr>",            desc = "Git branches" },
    },
    config = function()
      local telescope = require("telescope")
      telescope.setup({
        defaults = {
          path_display = { "smart" },
          layout_strategy = "horizontal",
          layout_config = { preview_width = 0.55 },
        },
      })
      telescope.load_extension("fzf")
    end,
  },

  -- -------------------------------------------------------------------------
  -- Treesitter (syntax highlighting + indent)
  -- -------------------------------------------------------------------------
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    event = { "BufReadPost", "BufNewFile" },
    config = function()
      require("nvim-treesitter").setup({
        ensure_installed = {
          "lua", "vim", "vimdoc",
          "python", "go", "javascript", "typescript", "tsx",
          "yaml", "json", "toml", "markdown", "markdown_inline",
          "bash", "dockerfile", "hcl",
        },
      })
    end,
  },

  -- -------------------------------------------------------------------------
  -- LSP (mason manages server installs)
  -- -------------------------------------------------------------------------
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "hrsh7th/cmp-nvim-lsp",
    },
    config = function()
      require("mason").setup()
      require("mason-lspconfig").setup({
        ensure_installed = {
          "gopls",      -- Go
          "pyright",    -- Python
          "ts_ls",      -- TypeScript/JavaScript
          "yamlls",     -- YAML (Kubernetes, GitHub Actions, etc.)
          "lua_ls",     -- Lua (this config)
          "dockerls",   -- Dockerfile
        },
        automatic_installation = true,
      })

      -- Keymaps set on every LSP attach (Neovim 0.11 style)
      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(args)
          local opts = { buffer = args.buf }
          map("n", "gd",         vim.lsp.buf.definition,     opts)
          map("n", "gD",         vim.lsp.buf.declaration,    opts)
          map("n", "gr",         vim.lsp.buf.references,     opts)
          map("n", "gi",         vim.lsp.buf.implementation, opts)
          map("n", "K",          vim.lsp.buf.hover,          opts)
          map("n", "<leader>rn", vim.lsp.buf.rename,         opts)
          map("n", "<leader>ca", vim.lsp.buf.code_action,    opts)
          map("n", "<leader>cf", vim.lsp.buf.format,         opts)
          map("i", "<C-k>",      vim.lsp.buf.signature_help, opts)
        end,
      })

      -- Global capabilities for all servers (Neovim 0.11 style)
      vim.lsp.config("*", {
        capabilities = require("cmp_nvim_lsp").default_capabilities(),
      })

      -- Per-server overrides
      vim.lsp.config("lua_ls", {
        settings = { Lua = { diagnostics = { globals = { "vim" } } } },
      })

      -- Enable servers (mason-lspconfig installs them, we just enable)
      vim.lsp.enable({ "gopls", "pyright", "ts_ls", "yamlls", "lua_ls", "dockerls" })

      -- Diagnostic display
      vim.diagnostic.config({
        virtual_text = { prefix = "●" },
        severity_sort = true,
        signs = true,
        underline = true,
        update_in_insert = false,
      })
    end,
  },

  -- -------------------------------------------------------------------------
  -- Completion
  -- -------------------------------------------------------------------------
  {
    "hrsh7th/nvim-cmp",
    event = "InsertEnter",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",
      "hrsh7th/cmp-buffer",
      "hrsh7th/cmp-path",
      "L3MON4D3/LuaSnip",
      "saadparwaiz1/cmp_luasnip",
      "rafamadriz/friendly-snippets",
    },
    config = function()
      local cmp = require("cmp")
      local luasnip = require("luasnip")
      require("luasnip.loaders.from_vscode").lazy_load()

      cmp.setup({
        snippet = {
          expand = function(args) luasnip.lsp_expand(args.body) end,
        },
        mapping = cmp.mapping.preset.insert({
          ["<C-n>"]     = cmp.mapping.select_next_item(),
          ["<C-p>"]     = cmp.mapping.select_prev_item(),
          ["<C-d>"]     = cmp.mapping.scroll_docs(-4),
          ["<C-f>"]     = cmp.mapping.scroll_docs(4),
          ["<C-Space>"] = cmp.mapping.complete(),
          ["<C-e>"]     = cmp.mapping.abort(),
          ["<CR>"]      = cmp.mapping.confirm({ select = true }),
          ["<Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
              cmp.select_next_item()
            elseif luasnip.expand_or_jumpable() then
              luasnip.expand_or_jump()
            else
              fallback()
            end
          end, { "i", "s" }),
          ["<S-Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
              cmp.select_prev_item()
            elseif luasnip.jumpable(-1) then
              luasnip.jump(-1)
            else
              fallback()
            end
          end, { "i", "s" }),
        }),
        sources = cmp.config.sources({
          { name = "nvim_lsp" },
          { name = "luasnip" },
          { name = "buffer" },
          { name = "path" },
        }),
      })
    end,
  },

  -- -------------------------------------------------------------------------
  -- Git integration (replaces vim-gitgutter)
  -- -------------------------------------------------------------------------
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPost", "BufNewFile" },
    opts = {
      signs = {
        add          = { text = "+" },
        change       = { text = "~" },
        delete       = { text = "_" },
        topdelete    = { text = "‾" },
        changedelete = { text = "~" },
      },
      on_attach = function(bufnr)
        local gs = package.loaded.gitsigns
        local opts = { buffer = bufnr }
        map("n", "]h",         gs.next_hunk,                                    opts)
        map("n", "[h",         gs.prev_hunk,                                    opts)
        map("n", "<leader>hs", gs.stage_hunk,                                   opts)
        map("n", "<leader>hr", gs.reset_hunk,                                   opts)
        map("n", "<leader>hp", gs.preview_hunk,                                 opts)
        map("n", "<leader>hb", function() gs.blame_line({ full = true }) end,   opts)
        map("n", "<leader>hd", gs.diffthis,                                     opts)
      end,
    },
  },

  -- -------------------------------------------------------------------------
  -- Which-key (shows available keybindings)
  -- -------------------------------------------------------------------------
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {
      plugins = { spelling = true },
    },
    config = function(_, opts)
      local wk = require("which-key")
      wk.setup(opts)
      wk.add({
        { "<leader>f", group = "find" },
        { "<leader>g", group = "git" },
        { "<leader>h", group = "hunks" },
        { "<leader>c", group = "code" },
        { "<leader>b", group = "buffer" },
      })
    end,
  },

  -- -------------------------------------------------------------------------
  -- Auto pairs
  -- -------------------------------------------------------------------------
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    opts = { check_ts = true },
    config = function(_, opts)
      local autopairs = require("nvim-autopairs")
      autopairs.setup(opts)
      -- Connect with cmp
      local cmp_autopairs = require("nvim-autopairs.completion.cmp")
      local cmp = require("cmp")
      cmp.event:on("confirm_done", cmp_autopairs.on_confirm_done())
    end,
  },

  -- -------------------------------------------------------------------------
  -- Comments
  -- -------------------------------------------------------------------------
  {
    "numToStr/Comment.nvim",
    event = { "BufReadPost", "BufNewFile" },
    opts = {},
  },

  -- -------------------------------------------------------------------------
  -- Auto-detect indentation
  -- -------------------------------------------------------------------------
  { "tpope/vim-sleuth" },

  -- -------------------------------------------------------------------------
  -- Indent guides
  -- -------------------------------------------------------------------------
  {
    "lukas-reineke/indent-blankline.nvim",
    main = "ibl",
    event = { "BufReadPost", "BufNewFile" },
    opts = {
      indent = { char = "│" },
      scope = { enabled = false },
    },
  },

  -- -------------------------------------------------------------------------
  -- Mini modules (misc quality-of-life)
  -- -------------------------------------------------------------------------
  {
    "echasnovski/mini.surround",
    version = "*",
    opts = {},
  },

}, {
  -- lazy.nvim options
  ui = { border = "rounded" },
  checker = { enabled = true, notify = false },
  change_detection = { notify = false },
})
