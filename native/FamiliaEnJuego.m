#import <Cocoa/Cocoa.h>
#import <WebKit/WebKit.h>

@interface AppDelegate : NSObject <NSApplicationDelegate, WKNavigationDelegate>
@property (strong) NSWindow *window;
@property (strong) WKWebView *webView;
@property (strong) NSTask *serverProcess;
@property (strong) NSURL *gameURL;
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)notification {
    [NSApp setActivationPolicy:NSApplicationActivationPolicyRegular];
    self.gameURL = [NSURL URLWithString:@"http://127.0.0.1:8765"];
    [self configureMenu];
    [self createWindow];
    [self startServer];
    [self waitForServer:0];
    [NSApp activateIgnoringOtherApps:YES];
}

- (void)configureMenu {
    NSMenu *mainMenu = [[NSMenu alloc] init];
    NSMenuItem *appItem = [[NSMenuItem alloc] init];
    [mainMenu addItem:appItem];
    NSMenu *appMenu = [[NSMenu alloc] initWithTitle:@"Familia en Juego"];
    [appMenu addItemWithTitle:@"Acerca de Familia en Juego" action:@selector(orderFrontStandardAboutPanel:) keyEquivalent:@""];
    [appMenu addItem:[NSMenuItem separatorItem]];
    NSMenuItem *reload = [[NSMenuItem alloc] initWithTitle:@"Recargar juego" action:@selector(reloadGame:) keyEquivalent:@"r"];
    reload.target = self;
    [appMenu addItem:reload];
    [appMenu addItem:[NSMenuItem separatorItem]];
    [appMenu addItemWithTitle:@"Cerrar Familia en Juego" action:@selector(terminate:) keyEquivalent:@"q"];
    appItem.submenu = appMenu;
    NSApp.mainMenu = mainMenu;
}

- (void)createWindow {
    WKWebViewConfiguration *configuration = [[WKWebViewConfiguration alloc] init];
    configuration.websiteDataStore = [WKWebsiteDataStore defaultDataStore];
    self.webView = [[WKWebView alloc] initWithFrame:NSZeroRect configuration:configuration];
    self.webView.navigationDelegate = self;

    NSRect frame = NSMakeRect(0, 0, 1280, 820);
    NSWindowStyleMask style = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable | NSWindowStyleMaskFullSizeContentView;
    self.window = [[NSWindow alloc] initWithContentRect:frame styleMask:style backing:NSBackingStoreBuffered defer:NO];
    self.window.title = @"Familia en Juego";
    self.window.titlebarAppearsTransparent = YES;
    self.window.titleVisibility = NSWindowTitleHidden;
    self.window.minSize = NSMakeSize(900, 620);
    self.window.contentView = self.webView;
    [self.window center];
    [self.window makeKeyAndOrderFront:nil];

    NSString *loading = @"<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0;background:#fffaf0;color:#1f1b38;font-family:-apple-system,sans-serif;display:grid;place-items:center;height:100vh;text-align:center}.die{font-size:64px;animation:bop 1s infinite alternate}@keyframes bop{to{transform:translateY(-12px) rotate(8deg)}}h2{margin:12px 0 4px}p{color:#746f8d}</style></head><body><div><div class='die'>🎲</div><h2>Preparando Familia en Juego…</h2><p>Encendiendo la diversión</p></div></body></html>";
    [self.webView loadHTMLString:loading baseURL:nil];
}

- (void)startServer {
    NSURL *resources = NSBundle.mainBundle.resourceURL;
    if (!resources) return;
    NSURL *script = [resources URLByAppendingPathComponent:@"server.py"];
    self.serverProcess = [[NSTask alloc] init];
    self.serverProcess.executableURL = [NSURL fileURLWithPath:@"/usr/bin/python3"];
    self.serverProcess.arguments = @[script.path];
    self.serverProcess.currentDirectoryURL = resources;
    NSMutableDictionary *environment = [NSProcessInfo.processInfo.environment mutableCopy];
    environment[@"FAMILIA_PORT"] = @"8765";
    environment[@"PYTHONUNBUFFERED"] = @"1";
    NSURL *support = [[[NSFileManager defaultManager] URLsForDirectory:NSApplicationSupportDirectory inDomains:NSUserDomainMask] firstObject];
    NSURL *dataDirectory = [support URLByAppendingPathComponent:@"Familia en Juego" isDirectory:YES];
    [[NSFileManager defaultManager] createDirectoryAtURL:dataDirectory withIntermediateDirectories:YES attributes:nil error:nil];
    environment[@"FAMILIA_DATA_DIR"] = dataDirectory.path;
    self.serverProcess.environment = environment;
    self.serverProcess.standardOutput = [NSFileHandle fileHandleWithNullDevice];
    self.serverProcess.standardError = [NSFileHandle fileHandleWithNullDevice];
    NSError *error = nil;
    if (![self.serverProcess launchAndReturnError:&error]) {
        [self showError:[NSString stringWithFormat:@"No se pudo iniciar el servidor local: %@", error.localizedDescription]];
    }
}

- (void)waitForServer:(NSInteger)attempt {
    if (attempt >= 40) {
        [self showError:@"El servidor tardó demasiado en responder. Cerrá la app y volvé a abrirla."];
        return;
    }
    NSURL *statusURL = [self.gameURL URLByAppendingPathComponent:@"api/state"];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:statusURL];
    request.timeoutInterval = 1;
    __weak AppDelegate *weakSelf = self;
    [[[NSURLSession sharedSession] dataTaskWithRequest:request completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        BOOL ready = [(NSHTTPURLResponse *)response statusCode] == 200;
        dispatch_async(dispatch_get_main_queue(), ^{
            AppDelegate *strongSelf = weakSelf;
            if (!strongSelf) return;
            if (ready) {
                [strongSelf.webView loadRequest:[NSURLRequest requestWithURL:strongSelf.gameURL]];
            } else {
                dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
                    [strongSelf waitForServer:attempt + 1];
                });
            }
        });
    }] resume];
}

- (void)reloadGame:(id)sender {
    [self.webView loadRequest:[NSURLRequest requestWithURL:self.gameURL]];
}

- (void)showError:(NSString *)message {
    NSAlert *alert = [[NSAlert alloc] init];
    alert.messageText = @"Familia en Juego";
    alert.informativeText = message;
    alert.alertStyle = NSAlertStyleWarning;
    [alert runModal];
}

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender { return YES; }

- (void)applicationWillTerminate:(NSNotification *)notification {
    if (self.serverProcess.running) [self.serverProcess terminate];
}
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSApplication *application = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        application.delegate = delegate;
        [application run];
    }
    return 0;
}
